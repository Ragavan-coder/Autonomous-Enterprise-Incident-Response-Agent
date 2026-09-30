import os
import glob
from typing import List, Dict
from openai import OpenAI
from app.config import settings
from app.database.connection import get_db_connection
import logging

logger = logging.getLogger(__name__)

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def get_embedding(text: str) -> List[float]:
    if not settings.OPENAI_API_KEY:
        # Return dummy embedding if no key is available for testing
        return [0.0] * 1536
    try:
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Failed to get embedding: {e}")
        return [0.0] * 1536

def ingest_runbooks():
    """Ingest markdown files from data/runbooks."""
    runbook_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "..", "data", "runbooks")
    files = glob.glob(os.path.join(runbook_dir, "*.md"))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            for file_path in files:
                filename = os.path.basename(file_path)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                doc_id = filename.replace(".md", "")
                
                # Insert document
                cur.execute("""
                    INSERT INTO documents (id, service, document_type, title, content)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                """, (doc_id, doc_id.split("-")[0] + "-service", "runbook", filename, content))
                
                # Simple chunking by paragraphs or double newlines
                chunks = [c.strip() for c in content.split("\n\n") if c.strip()]
                for i, chunk in enumerate(chunks):
                    chunk_id = f"{doc_id}-chunk-{i}"
                    emb = get_embedding(chunk)
                    
                    cur.execute("""
                        INSERT INTO document_chunks (id, document_id, section, content, embedding)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO NOTHING
                    """, (chunk_id, doc_id, f"Section {i}", chunk, emb))
        conn.commit()
    except Exception as e:
        logger.error(f"Error during ingestion: {e}")
        conn.rollback()
    finally:
        conn.close()

def retrieve_context(query: str, top_k: int = 3) -> List[Dict[str, str]]:
    query_emb = get_embedding(query)
    conn = get_db_connection()
    results = []
    try:
        with conn.cursor() as cur:
            # Requires pgvector to be enabled and table to have vector type
            # Using cosine similarity (<=>)
            cur.execute("""
                SELECT c.content, c.section, d.title 
                FROM document_chunks c
                JOIN documents d ON c.document_id = d.id
                ORDER BY c.embedding <=> %s::vector
                LIMIT %s
            """, (query_emb, top_k))
            rows = cur.fetchall()
            for r in rows:
                results.append({
                    "content": r["content"],
                    "section": r["section"],
                    "document": r["title"]
                })
    except Exception as e:
        logger.error(f"Error during retrieval: {e}")
    finally:
        conn.close()
    return results

import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from app.config import settings

logger = logging.getLogger(__name__)

def get_db_connection():
    try:
        conn = psycopg2.connect(
            settings.DATABASE_URL,
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        raise

def initialize_database():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # Enable pgvector
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            
            # Create schema
            cur.execute("""
            CREATE TABLE IF NOT EXISTS incidents (
                id VARCHAR(255) PRIMARY KEY,
                title VARCHAR(255),
                description TEXT,
                service VARCHAR(255),
                severity VARCHAR(50),
                status VARCHAR(50),
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                investigation_duration FLOAT
            );
            
            CREATE TABLE IF NOT EXISTS incident_events (
                id VARCHAR(255) PRIMARY KEY,
                incident_id VARCHAR(255),
                timestamp TIMESTAMP,
                actor VARCHAR(255),
                event VARCHAR(255),
                details TEXT
            );

            CREATE TABLE IF NOT EXISTS documents (
                id VARCHAR(255) PRIMARY KEY,
                service VARCHAR(255),
                document_type VARCHAR(255),
                title VARCHAR(255),
                content TEXT
            );

            CREATE TABLE IF NOT EXISTS document_chunks (
                id VARCHAR(255) PRIMARY KEY,
                document_id VARCHAR(255),
                section VARCHAR(255),
                content TEXT,
                embedding vector(1536)
            );
            
            CREATE TABLE IF NOT EXISTS previous_incidents (
                id VARCHAR(255) PRIMARY KEY,
                service VARCHAR(255),
                root_cause TEXT,
                resolution TEXT
            );
            
            CREATE TABLE IF NOT EXISTS audit_logs (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP,
                actor VARCHAR(255),
                event VARCHAR(255),
                incident_id VARCHAR(255),
                details TEXT
            );
            """)
        conn.commit()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        conn.rollback()
    finally:
        conn.close()

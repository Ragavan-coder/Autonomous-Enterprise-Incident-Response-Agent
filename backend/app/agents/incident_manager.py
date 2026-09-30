import json
import time
from typing import Dict, Any, List
from openai import OpenAI
from app.config import settings
from app.tools.registry import TOOLS_SCHEMA, TOOL_REGISTRY

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def trigger_investigation(incident: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Orchestrate the investigation using the OpenAI agent with tool calling.
    """
    if not settings.OPENAI_API_KEY:
        # Dummy trace for testing without API key
        return [{"step": "planner", "action": "Skipped due to missing API key"}]
        
    messages = [
        {
            "role": "system",
            "content": (
                "You are an Autonomous Enterprise Incident Response Agent (AIRA). "
                "Your job is to investigate production incidents using tools. "
                "Never invent evidence. Use tools to gather data. "
                "Do not make destructive changes. Formulate a root cause based on evidence."
            )
        },
        {
            "role": "user",
            "content": f"Investigate this incident:\nTitle: {incident.get('title')}\nDescription: {incident.get('description')}\nService: {incident.get('service')}"
        }
    ]
    
    trace = []
    step_count = 0
    
    while step_count < settings.MAX_AGENT_STEPS:
        step_count += 1
        
        response = client.chat.completions.create(
            model="gpt-4o",  # or gpt-4o-mini
            messages=messages,
            tools=TOOLS_SCHEMA,
            tool_choice="auto",
            max_tokens=2048
        )
        
        message = response.choices[0].message
        
        if message.content:
            trace.append({
                "agent": "investigator",
                "content": message.content,
                "timestamp": time.time()
            })
            messages.append({"role": "assistant", "content": message.content})
            
        if not message.tool_calls:
            # Agent decided it's done
            break
            
        # Add the assistant's tool calls to messages
        messages.append(message)
        
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            
            trace.append({
                "agent": "tool_execution",
                "tool": tool_name,
                "args": args,
                "timestamp": time.time()
            })
            
            if tool_name in TOOL_REGISTRY:
                try:
                    result = TOOL_REGISTRY[tool_name](**args)
                    str_result = json.dumps(result)
                except Exception as e:
                    str_result = f"Error: {e}"
            else:
                str_result = f"Unknown tool: {tool_name}"
                
            trace.append({
                "agent": "tool_result",
                "tool": tool_name,
                "result": str_result,
                "timestamp": time.time()
            })
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_name,
                "content": str_result
            })
            
    # Final Root Cause Analysis Step using Structured Output
    root_cause_prompt = {
        "role": "user",
        "content": "Based on the investigation, provide the root cause analysis and remediation proposal using the required JSON schema."
    }
    messages.append(root_cause_prompt)
    
    try:
        final_res = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            response_format={ "type": "json_object" } # Simplified for demo, proper schema in production
        )
        trace.append({
            "agent": "root_cause_analyzer",
            "content": final_res.choices[0].message.content,
            "timestamp": time.time()
        })
    except Exception as e:
        trace.append({"agent": "root_cause_analyzer", "error": str(e)})

    return trace

from typing import List, Dict, Any
from datetime import datetime, timedelta
import json

def get_dependencies(service: str) -> Dict[str, Any]:
    from app.graph.graph import service_graph
    
    deps = service_graph.bfs(service)
    return {
        "service": service,
        "dependencies": deps
    }

def search_logs(service: str, start_time: str, end_time: str, severity: str = "ERROR", keyword: str = "") -> List[Dict[str, str]]:
    # Simulated logs based on service and keywords
    logs = []
    
    if service == "payment-service" and ("database connection pool" in keyword.lower() or keyword == ""):
        logs.append({
            "timestamp": (datetime.utcnow() - timedelta(minutes=5)).isoformat(),
            "service": "payment-service",
            "severity": "ERROR",
            "message": "Database connection pool exhausted"
        })
        logs.append({
            "timestamp": (datetime.utcnow() - timedelta(minutes=4)).isoformat(),
            "service": "payment-service",
            "severity": "ERROR",
            "message": "Timeout connecting to postgres-payment"
        })
        
    if service == "checkout-service":
        logs.append({
            "timestamp": (datetime.utcnow() - timedelta(minutes=3)).isoformat(),
            "service": "checkout-service",
            "severity": "ERROR",
            "message": "Failed to call payment-service, connection reset"
        })
        
    if service == "postgres-payment":
        logs.append({
            "timestamp": (datetime.utcnow() - timedelta(minutes=6)).isoformat(),
            "service": "postgres-payment",
            "severity": "WARNING",
            "message": "Max connections reached"
        })

    return logs

def get_metrics(service: str, metric: str, start_time: str, end_time: str) -> Dict[str, Any]:
    # Simulated metrics
    if service == "checkout-service" and metric == "error_rate":
        return {"service": service, "metric": metric, "value": "18%"}
    elif service == "payment-service" and metric == "latency":
        return {"service": service, "metric": metric, "value": "840ms"}
    elif service == "postgres-payment" and metric == "database_connections":
        return {"service": service, "metric": metric, "value": "98%"}
        
    return {"service": service, "metric": metric, "value": "normal"}

def check_service_health(service: str) -> Dict[str, Any]:
    if service == "payment-service":
        return {"service": service, "status": "DEGRADED", "latency_ms": 840, "error_rate": 0.18}
    if service == "checkout-service":
        return {"service": service, "status": "DEGRADED", "latency_ms": 120, "error_rate": 0.18}
    if service == "postgres-payment":
        return {"service": service, "status": "DEGRADED", "latency_ms": 50, "error_rate": 0.05}
    return {"service": service, "status": "HEALTHY", "latency_ms": 20, "error_rate": 0.001}

def get_recent_deployments(service: str) -> List[Dict[str, str]]:
    if service == "payment-service":
        return [
            {"version": "v4.8.2", "deployed_at": (datetime.utcnow() - timedelta(minutes=7)).isoformat(), "status": "SUCCESS"},
            {"version": "v4.8.1", "deployed_at": (datetime.utcnow() - timedelta(days=2)).isoformat(), "status": "SUCCESS"}
        ]
    return []

# Central schema definition for OpenAI function calling
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_dependencies",
            "description": "Get the downstream service dependencies using BFS.",
            "parameters": {
                "type": "object",
                "properties": {
                    "service": {"type": "string"}
                },
                "required": ["service"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_logs",
            "description": "Search logs for a specific service and timeframe.",
            "parameters": {
                "type": "object",
                "properties": {
                    "service": {"type": "string"},
                    "start_time": {"type": "string"},
                    "end_time": {"type": "string"},
                    "severity": {"type": "string"},
                    "keyword": {"type": "string"}
                },
                "required": ["service", "start_time", "end_time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_metrics",
            "description": "Get timeseries metrics for a service.",
            "parameters": {
                "type": "object",
                "properties": {
                    "service": {"type": "string"},
                    "metric": {"type": "string", "enum": ["latency", "error_rate", "request_rate", "cpu", "memory", "database_connections", "queue_depth"]},
                    "start_time": {"type": "string"},
                    "end_time": {"type": "string"}
                },
                "required": ["service", "metric", "start_time", "end_time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_service_health",
            "description": "Check current health status of a service.",
            "parameters": {
                "type": "object",
                "properties": {
                    "service": {"type": "string"}
                },
                "required": ["service"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_recent_deployments",
            "description": "Get recent deployments for a given service.",
            "parameters": {
                "type": "object",
                "properties": {
                    "service": {"type": "string"}
                },
                "required": ["service"]
            }
        }
    }
]

TOOL_REGISTRY = {
    "get_dependencies": get_dependencies,
    "search_logs": search_logs,
    "get_metrics": get_metrics,
    "check_service_health": check_service_health,
    "get_recent_deployments": get_recent_deployments
}

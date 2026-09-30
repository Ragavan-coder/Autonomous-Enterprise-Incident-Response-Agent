from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_services():
    from app.graph.graph import service_graph
    return {"services": list(service_graph.edges.keys())}

@router.get("/{name}/dependencies")
def get_service_dependencies(name: str):
    from app.graph.graph import service_graph
    deps = service_graph.bfs(name)
    return {"service": name, "dependencies": deps}

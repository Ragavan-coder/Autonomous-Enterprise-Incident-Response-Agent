import heapq
from typing import Dict, List, Optional, Tuple

class ServiceGraph:
    def __init__(self):
        # adjacency list: node -> { neighbor: weight }
        self.edges: Dict[str, Dict[str, float]] = {}

    def add_edge(self, u: str, v: str, latency: float = 1.0):
        if u not in self.edges:
            self.edges[u] = {}
        if v not in self.edges:
            self.edges[v] = {}
        self.edges[u][v] = latency

    def bfs(self, start: str) -> List[str]:
        if start not in self.edges:
            return []
        visited = set([start])
        queue = [start]
        result = []
        
        while queue:
            node = queue.pop(0)
            result.append(node)
            for neighbor in self.edges.get(node, {}):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return result

    def dfs(self, start: str) -> List[str]:
        if start not in self.edges:
            return []
        visited = set()
        result = []
        
        def _dfs(node: str):
            if node in visited:
                return
            visited.add(node)
            result.append(node)
            for neighbor in self.edges.get(node, {}):
                _dfs(neighbor)
                
        _dfs(start)
        return result

    def dijkstra(self, start: str, target: str) -> Tuple[Optional[List[str]], float]:
        if start not in self.edges or target not in self.edges:
            return None, float('inf')
            
        distances = {node: float('inf') for node in self.edges}
        distances[start] = 0
        previous = {node: None for node in self.edges}
        
        pq = [(0, start)]
        
        while pq:
            current_dist, current_node = heapq.heappop(pq)
            
            if current_node == target:
                break
                
            if current_dist > distances[current_node]:
                continue
                
            for neighbor, weight in self.edges[current_node].items():
                distance = current_dist + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))
                    
        if distances[target] == float('inf'):
            return None, float('inf')
            
        path = []
        curr = target
        while curr is not None:
            path.append(curr)
            curr = previous[curr]
            
        return path[::-1], distances[target]

# Singleton instance
service_graph = ServiceGraph()

# Build the predefined graph
def initialize_graph():
    # api-gateway -> auth, checkout
    service_graph.add_edge("api-gateway", "auth-service", 10)
    service_graph.add_edge("api-gateway", "checkout-service", 20)
    
    # checkout -> orders, payment
    service_graph.add_edge("checkout-service", "order-service", 30)
    service_graph.add_edge("checkout-service", "payment-service", 40)
    
    # payment -> db, inventory
    service_graph.add_edge("payment-service", "postgres-payment", 5)
    service_graph.add_edge("payment-service", "inventory-service", 15)
    
    # orders -> kafka
    service_graph.add_edge("order-service", "kafka-orders", 10)
    
    # add other nodes just to be safe
    for s in ["user-service", "notification-service", "search-service", 
              "recommendation-service", "analytics-service", "redis-cache"]:
        if s not in service_graph.edges:
            service_graph.edges[s] = {}

initialize_graph()

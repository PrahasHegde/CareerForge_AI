from streamlit_agraph import Node, Edge, Config

def build_skill_graph(present_skills, missing_skills):
    nodes = []
    edges = []
    
    # 1. Central Node (The Candidate)
    # Using a simple ID and Label, avoiding image URLs to prevent Windows errors
    nodes.append(Node(
        id="Candidate", 
        label=" YOU ", 
        size=40, 
        color="#2196F3",
    ))
    
    # 2. Present Skills (Green)
    for skill in present_skills:
        nodes.append(Node(id=skill, label=skill, size=20, color="#4CAF50"))
        edges.append(Edge(source="Candidate", target=skill, color="#4CAF50", label="HAS"))
        
    # 3. Missing Skills (Red)
    for skill in missing_skills:
        nodes.append(Node(id=skill, label=skill, size=20, color="#FF5252"))
        edges.append(Edge(source="Candidate", target=skill, color="#FF5252", label="MISSING"))
        
    # 4. Configuration
    config = Config(
        width=800, 
        height=500, 
        directed=True, 
        nodeHighlightBehavior=True, 
        highlightColor="#F7A7A6",
        collapsible=True,
        physics={
            "enabled": True,
            "stabilization": {"enabled": True}
        }
    )
    return nodes, edges, config
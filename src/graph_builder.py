from streamlit_agraph import Node, Edge, Config

def build_skill_graph(present_skills, missing_skills):
    """
    Build a professional, clean skill graph with improved visual hierarchy.
    """
    nodes = []
    edges = []
    
    # 1. Central Node (You) - Premium styling
    nodes.append(Node(
        id="YOU",
        label="YOU",
        size=50,
        color="#6366f1",
        borderWidth=3,
        borderColor="#818cf8",
        font={"size": 18, "color": "#ffffff", "bold": {"color": "#ffffff"}}
    ))
    
    # 2. Present Skills (Green - what you have)
    for i, skill in enumerate(present_skills):
        nodes.append(Node(
            id=f"present_{i}_{skill}",
            label=skill,
            size=28,
            color="#10b981",
            borderWidth=2,
            borderColor="#34d399",
            font={"size": 13, "color": "#ffffff", "bold": {"color": "#ffffff"}},
            title=f"✅ You have: {skill}"
        ))
        edges.append(Edge(
            source="YOU",
            target=f"present_{i}_{skill}",
            color="#10b981",
            width=2.5,
            label="HAVE",
            font={"size": 11, "color": "#10b981"},
            smooth={"type": "continuous"}
        ))
    
    # 3. Missing Skills (Orange - skills to learn)
    for i, skill in enumerate(missing_skills):
        nodes.append(Node(
            id=f"missing_{i}_{skill}",
            label=skill,
            size=26,
            color="#f59e0b",
            borderWidth=2,
            borderColor="#fbbf24",
            font={"size": 13, "color": "#ffffff", "bold": {"color": "#ffffff"}},
            title=f"⚠️ Learn: {skill}"
        ))
        edges.append(Edge(
            source="YOU",
            target=f"missing_{i}_{skill}",
            color="#f59e0b",
            width=2.5,
            label="NEED",
            font={"size": 11, "color": "#f59e0b"},
            smooth={"type": "continuous"}
        ))
    
    # 4. Enhanced Configuration - Professional & Clean
    config = Config(
        width=1000,
        height=600,
        directed=True,
        nodeHighlightBehavior=True,
        highlightColor="#a78bfa",
        collapsible=False,
        node={
            "labelProperty": "label",
            "renderLabel": True,
            "highlightStrokeColor": "#a78bfa"
        },
        link={
            "highlightColor": "#a78bfa",
            "renderLabel": True,
            "fontSize": 11
        },
        physics={
            "enabled": True,
            "barnesHut": {
                "theta": 0.5,
                "gravitationalConstant": -35000,
                "centralGravity": 0.3,
                "springLength": 250,
                "springConstant": 0.04,
                "damping": 0.09,
                "avoidOverlap": 0.2
            },
            "maxVelocity": 50,
            "solver": "barnesHut",
            "timestep": 0.35,
            "stabilization": {
                "iterations": 200,
                "fit": True,
                "updateInterval": 25
            }
        }
    )
    
    return nodes, edges, config
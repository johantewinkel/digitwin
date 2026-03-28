import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
import plotly.graph_objects as go

def tqm_analysis(waiting_times):
    avg = {k: np.mean(v) for k,v in waiting_times.items()}
    df = pd.DataFrame(avg.items(), columns=["Task","Waiting"])
    df = df.sort_values("Waiting", ascending=False)

    st.bar_chart(df.set_index("Task"))
    st.warning(f"Bottleneck: {df.iloc[0]['Task']}")

def visualize_workflow_graph(workflow):
    G = nx.DiGraph()

    for n in workflow["nodes"]:
        G.add_node(n["name"])

    for e in workflow["edges"]:
        label = e.get("label", "")
        G.add_edge(e["from"], e["to"], label=label)

    pos = nx.spring_layout(G)

    fig = go.Figure()

    for edge in G.edges():
        x0,y0 = pos[edge[0]]
        x1,y1 = pos[edge[1]]
        fig.add_trace(go.Scatter(x=[x0,x1], y=[y0,y1], mode='lines'))

    for node in G.nodes():
        x,y = pos[node]
        fig.add_trace(go.Scatter(x=[x], y=[y], text=node, mode='markers+text'))

    st.plotly_chart(fig)
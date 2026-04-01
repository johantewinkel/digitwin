import streamlit as st
import pandas as pd
import numpy as np

from simulator_should import simulate_process
from rl_agent import run_rl
from analytics import tqm_analysis, visualize_workflow_graph
from excel_utils import export_workflow_to_excel, import_workflow_from_excel
from process_mining import extract_parameters_from_event_log
import config

st.set_page_config(layout="wide")

st.title("💡 Digivatie Digital Twin Platform")
st.caption("Simulate • Optimize • Redesign")

# ---------------- SIDEBAR ----------------
mode = st.sidebar.radio("Input type", [
    "Demo",
    "Excel parameters",
    "Event log (process mining)"
])

n_cases = st.sidebar.slider("Aantal cases", 1, 100, 20)

# Scenario planning
st.sidebar.markdown("## 📊 Scenario Planning")
volume_factor = st.sidebar.slider("Volume (cases)", 0.5, 2.0, 1.0)
resource_factor = st.sidebar.slider("Resources scaling", 0.5, 2.0, 1.0)
humidity_input = st.sidebar.slider("Humidity", 0.0, 1.0, 0.5)
urgency_input = st.sidebar.slider("Urgency", 1, 5, 3)

# ---------------- DATA LOAD ----------------
if mode == "Demo":
    workflow = config.WASMACHINE_WORKFLOW
  #  task_times = {n["name"]: 10 for n in workflow["nodes"]}
  #  waiting = {n["name"]: 1 for n in workflow["nodes"]}
  #  costs = {n["name"]: 10 for n in workflow["nodes"]}
  #  resources = {n["name"]: 1 for n in workflow["nodes"]}
    task_times = {n["name"]: n.get("duration", 10) for n in workflow["nodes"]}
    waiting = {n["name"]: n.get("waiting", 10) for n in workflow["nodes"]}
    costs = {n["name"]: n.get("cost", 10) for n in workflow["nodes"]}
    resources = {n["name"]: n.get("resources", 10) for n in workflow["nodes"]}


elif mode == "Excel parameters":
    file = st.file_uploader("Upload Excel", type=["xlsx"])
    if file:
        task_times, waiting, costs, resources = import_workflow_from_excel(file)
        workflow = {"nodes":[{"name":k} for k in task_times], "edges":[]}

elif mode == "Event log (process mining)":
    file = st.file_uploader("Upload Event Log", type=["xlsx"])
    if file:
        task_times, waiting, costs, resources = extract_parameters_from_event_log(file)
        workflow = {"nodes":[{"name":k} for k in task_times], "edges":[]}

# ---------------- APPLY SCENARIO ----------------
if "task_times" in locals():

    scaled_cases = int(n_cases * volume_factor)
    scaled_resources = {k: max(1, int(v * resource_factor)) for k,v in resources.items()}

    # ---------------- TABS ----------------
    tab1, tab2, tab3, tab4 = st.tabs([
        "Workflow",
        "Simulation",
        "Bottlenecks",
        "Optimization"
    ])

    # ---------------- WORKFLOW ----------------
    with tab1:
        visualize_workflow_graph(workflow)

        if st.button("📤 Export workflow template"):
            file = export_workflow_to_excel(workflow)
            with open(file, "rb") as f:
                st.download_button("Download Excel", f, file_name=file)

    # ---------------- SIMULATION ----------------
    with tab2:
        if st.button("🚀 Run Simulation"):

            result = simulate_process(task_times, scaled_resources, scaled_cases, manual_waiting=waiting, workflow=workflow)

            st.metric("Doorlooptijd", round(result["avg_total_time"],1))
            st.metric("Wachttijd", round(result["avg_waiting_time"],1))
            st.metric("Cases", scaled_cases)

            tqm_analysis(result["waiting_times"])

    # ---------------- BOTTLENECKS ----------------
    with tab3:
        result = simulate_process(
            task_times, 
            scaled_resources, 
            scaled_cases, 
            manual_waiting=waiting, 
            workflow=workflow,
            context_override={
                "humidity": humidity_input,
                "urgency": urgency_input
            }
        )
        tqm_analysis(result["waiting_times"])

    # ---------------- OPTIMIZATION ----------------
    with tab4:
        if st.button("🤖 Run RL Optimization"):

            result = run_rl(
                task_times,
                scaled_resources,
                costs,
                waiting,
                scaled_cases,
                w_time=1.0,
                w_wait=0.5,
                w_cost=0.2
            )

            st.success(f"Nieuwe doorlooptijd: {result['time']}")

            df = pd.DataFrame(result["table"])
            st.dataframe(df)

            df.to_excel("optimized.xlsx", index=False)
            st.success("Excel export klaar!")
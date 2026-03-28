import pandas as pd

def export_workflow_to_excel(workflow, filename="workflow_input.xlsx"):
    data = []

    for node in workflow["nodes"]:
        data.append({
            "Task": node["name"],
            "Duration": 10,
            "Waiting": 1,
            "Cost": 10,
            "Resources": 1
        })

    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

    return filename


def import_workflow_from_excel(file):
    df = pd.read_excel(file)

    task_times = dict(zip(df["Task"], df["Duration"]))
    waiting = dict(zip(df["Task"], df["Waiting"]))
    costs = dict(zip(df["Task"], df["Cost"]))
    resources = dict(zip(df["Task"], df["Resources"]))

    return task_times, waiting, costs, resources
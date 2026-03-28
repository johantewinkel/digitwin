import pandas as pd

def extract_parameters_from_event_log(file):

    df = pd.read_excel(file)
    df = df.sort_values(["CaseID", "Timestamp"])

    durations = {}
    waiting = {}

    grouped = df.groupby("CaseID")

    for _, group in grouped:

        prev_time = None

        for _, row in group.iterrows():
            act = row["Activity"]
            time = row["Timestamp"]

            if prev_time is not None:
                delta = (time - prev_time).total_seconds() / 60
                waiting.setdefault(act, []).append(delta)

            prev_time = time

    for act in df["Activity"].unique():
        durations[act] = 10
        waiting[act] = sum(waiting.get(act, [0])) / max(len(waiting.get(act, [1])),1)

    resources = {act:1 for act in durations}
    costs = {act:10 for act in durations}

    return durations, waiting, costs, resources
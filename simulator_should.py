import simpy
import numpy as np
import random

def simulate_process(task_times, resources, n_cases, manual_waiting=None):

    env = simpy.Environment()

    res = {k: simpy.Resource(env, capacity=resources[k]) for k in task_times}

    waiting_times = {k: [] for k in task_times}
    total_times = []

    def process():

        current = list(task_times.keys())[0]  # startnode
        start = env.now
        st.write("current node:", current)

        while current:

            node = current
            st.write("current node:", current)

            # decision node
            node_config = next(n for n in workflow["nodes"] if n["name"] == node)

            if node_config.get("type") == "decision":

                probs = node_config["probabilities"]
                choice = random.choices(list(probs.keys()), weights=probs.values())[0]

                # vind juiste edge
                next_edges = [
                    e for e in workflow["edges"]
                    if e["from"] == node and e.get("label") == choice
                ]
                
                current = next_edges[0]["to"] if next_edges else None
                st.write("current node:", current)
                continue

            # normale task
            with res[node].request() as req:
                req_time = env.now
                yield req

                wait = env.now - req_time
                waiting_times[node].append(wait)

                yield env.timeout(task_times[node])

            # volgende stap
            next_edges = [e for e in workflow["edges"] if e["from"] == node]

            current = next_edges[0]["to"] if next_edges else None

        total_times.append(env.now - start)

    for _ in range(n_cases):
        env.process(process())

    env.run()

    return {
        "avg_total_time": np.mean(total_times),
        "avg_waiting_time": np.mean([np.mean(v) for v in waiting_times.values()]),
        "waiting_times": waiting_times
    }


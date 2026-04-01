import simpy
import numpy as np
import random
from decision_engine import decide

def simulate_process(task_times, resources, n_cases, manual_waiting=None, workflow=None, context_override=None):

    env = simpy.Environment()

    res = {k: simpy.Resource(env, capacity=resources[k]) for k in task_times}

    waiting_times = {k: [] for k in task_times}
    total_times = []

    def process():

        # voorbeeld context (kan uit data komen!)
        if context_override:
            context = context_override
        context = {
            "humidity": random.uniform(0,1),
            "urgency": random.randint(1,5)
        }

        current = workflow["nodes"][0]["name"]
        start = env.now

        while current:

            node_config = next(n for n in workflow["nodes"] if n["name"] == current)

            # ---- DECISION NODE ----
            if node_config.get("type") == "decision":

                decision = decide(node_config, context)

                next_edges = [
                    e for e in workflow["edges"]
                    if e["from"] == current and e.get("label") == decision
                ]

                current = next_edges[0]["to"] if next_edges else None
                continue

            # ---- NORMAL TASK ----
            with res[current].request() as req:
                req_time = env.now
                yield req

                wait = env.now - req_time

                if manual_waiting:
                    wait += manual_waiting.get(current, 0)

                waiting_times[current].append(wait)

                yield env.timeout(task_times[current])

            next_edges = [e for e in workflow["edges"] if e["from"] == current]
            current = next_edges[0]["to"] if next_edges else None
        #print("Tijd: ", env.now, " ", start)
        total_times.append(env.now - start)
        
    for _ in range(n_cases):
        env.process(process())

    env.run()
    valid_waiting = [ np.mean(v) for v in waiting_times.values() if len(v) > 0]

    print("total: ", [np.mean(v) for v in waiting_times.values()])
    return {
        "avg_total_time": np.mean(total_times) if total_times else 0,
        "avg_waiting_time": np.mean(valid_waiting) if valid_waiting else 0,
        "waiting_times": waiting_times
    }
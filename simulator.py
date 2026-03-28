import simpy
import numpy as np

def simulate_process(task_times, resources, n_cases, manual_waiting=None):

    env = simpy.Environment()

    res = {k: simpy.Resource(env, capacity=resources[k]) for k in task_times}

    waiting_times = {k: [] for k in task_times}
    total_times = []

    def process():
        start = env.now

        for t in task_times:
            with res[t].request() as req:
                req_time = env.now
                yield req

                wait = env.now - req_time

                if manual_waiting:
                    wait += manual_waiting.get(t, 0)

                waiting_times[t].append(wait)

                yield env.timeout(task_times[t])

        total_times.append(env.now - start)

    for _ in range(n_cases):
        env.process(process())

    env.run()

    return {
        "avg_total_time": np.mean(total_times),
        "avg_waiting_time": np.mean([np.mean(v) for v in waiting_times.values()]),
        "waiting_times": waiting_times
    }
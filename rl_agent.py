import numpy as np
from stable_baselines3 import PPO
import gymnasium as gym

from simulator import simulate_process

class Env(gym.Env):
    def __init__(self, times, resources, costs, waiting, n_cases, w_time, w_wait, w_cost):
        super().__init__()

        self.tasks = list(times.keys())
        self.times = times
        self.resources = resources
        self.costs = costs
        self.waiting = waiting
        self.n_cases = n_cases

        self.w_time = w_time
        self.w_wait = w_wait
        self.w_cost = w_cost

        self.action_space = gym.spaces.MultiDiscrete([3]*len(self.tasks))
        self.observation_space = gym.spaces.Box(
            low=0, high=100, shape=(len(self.tasks)*2,), dtype=np.float32
        )

    def reset(self, seed=None, options=None):
        state = list(self.times.values()) + list(self.resources.values())
        return np.array(state, dtype=np.float32), {}

    def step(self, action):
        times = self.times.copy()
        res = self.resources.copy()

        for i, a in enumerate(action):
            t = self.tasks[i]
            if a == 1:
                times[t] *= 0.8
            elif a == 2:
                res[t] += 1

        sim = simulate_process(times, res, self.n_cases, self.waiting)

        reward = -(
            self.w_time * sim["avg_total_time"] +
            self.w_wait * sim["avg_waiting_time"] +
            self.w_cost * sum(res.values())
        )

        state = list(times.values()) + list(res.values())

        return np.array(state), reward, True, False, {}

def run_rl(times, resources, costs, waiting, n_cases, w_time, w_wait, w_cost):

    env = Env(times, resources, costs, waiting, n_cases, w_time, w_wait, w_cost)

    model = PPO("MlpPolicy", env, verbose=0)
    model.learn(total_timesteps=5000)

    obs, _ = env.reset()
    action, _ = model.predict(obs)

    new_times = times.copy()
    new_res = resources.copy()

    for i, a in enumerate(action):
        t = list(times.keys())[i]
        if a == 1:
            new_times[t] *= 0.8
        elif a == 2:
            new_res[t] += 1

    result = simulate_process(new_times, new_res, n_cases, waiting)

    table = []
    for t in new_times:
        table.append({
            "Task": t,
            "Time": new_times[t],
            "Resources": new_res[t],
            "Cost": costs[t]
        })

    return {
        "time": round(result["avg_total_time"],1),
        "waiting_times": result["waiting_times"],
        "table": table
    }
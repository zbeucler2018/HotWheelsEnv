import gymnasium as gym
import numpy as np


class RewardOnCrash(gym.Wrapper):
    """
    A wrapper that rewards the agent when it fails a trick.
    """

    def __init__(self, env, r: float):
        super().__init__(env)
        self.crash_reward = r
        self.crash_threshold = 238

    def step(self, action):
        observation, reward, terminated, truncated, info = self.env.step(action)
        if observation.mean() >= self.crash_threshold:
            reward += self.crash_reward

        return observation, reward, terminated, truncated, info


class RewardOnWallCrash(gym.Wrapper):
    """
    A wrapper that rewards the agent when it crashes into a wall.
    """

    def __init__(self, env, r: float):
        super().__init__(env)
        self.wall_crash_reward = r

    def step(self, action):
        observation, reward, terminated, truncated, info = self.env.step(action)
        if info["hit_wall"] == 1:
            reward += self.wall_crash_reward

        return observation, reward, terminated, truncated, info


class ClipReward(gym.RewardWrapper):
    """
    Clip the reward to {+1, 0, -1} by its sign.
    """

    def __init__(self, env: gym.Env) -> None:
        super().__init__(env)

    def reward(self, reward: float) -> float:
        return np.sign(float(reward))
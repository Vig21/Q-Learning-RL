# -*- coding: utf-8 -*-
"""CartPole RL.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1-s4woDPMrz5hci5_cu3diNSNmTtEcPMq
"""

import gymnasium as gym # openai RL environment
import numpy as np

# Initialize Gym environment
env = gym.make("CartPole-v1") # can be rendered

def discretize(obs, bins):
    upper_bounds = [env.observation_space.high[0], 0.5, env.observation_space.high[2], np.radians(50)]
    lower_bounds = [env.observation_space.low[0], -0.5, env.observation_space.low[2], -np.radians(50)]
    ratios = [(obs[i] + abs(lower_bounds[i])) / (upper_bounds[i] - lower_bounds[i]) for i in range(len(obs))]
    discretized = [int(round((bins[i] - 1) * ratios[i])) for i in range(len(obs))]
    discretized = [min(bins[i] - 1, max(0, discretized[i])) for i in range(len(obs))]
    return tuple(discretized)

# Hyperparameters
episodes = 1000
learning_rate = 0.1
discount_factor = 0.95
epsilon = 1.0  # Exploration factor
epsilon_decay = 0.995
epsilon_min = 0.01

# discrete bins per state dimension
bins = [6, 12, 6, 12]

# Initialize the Q-table
q_table = np.zeros(bins + [env.action_space.n])

# Training
for episode in range(episodes):
    state = discretize(env.reset()[0], bins)
    done = False
    total_reward = 0

    while not done:

        if np.random.random() < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(q_table[state])

        obs, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated
        new_state = discretize(obs, bins)

        # Updating the Q learning
        q_table[state][action] += learning_rate * (reward + discount_factor * np.max(q_table[new_state]) - q_table[state][action])

        state = new_state
        total_reward += reward

    # Decay epsilon
    epsilon = max(epsilon_min, epsilon * epsilon_decay)

    if episode % 100 == 0:
        print(f"Episode: {episode}, Reward: {total_reward}")

print("Training completed!")

# Final policy
state = discretize(env.reset()[0], bins)
done = False
while not done:
    env.render()
    action = np.argmax(q_table[state])
    obs, _, terminated, truncated, _ = env.step(action)
    done = terminated or truncated
    state = discretize(obs, bins)

env.close()


import numpy as np
import random
from config import Config

class QLearningAgent:
    def __init__(self, state_space_size, action_space_size):
        self.state_space_size = state_space_size
        self.action_space_size = action_space_size
        self.learning_rate = Config.LEARNING_RATE
        self.discount_factor = Config.DISCOUNT_FACTOR
        self.exploration_rate = Config.EXPLORATION_RATE
        self.exploration_decay = Config.EXPLORATION_DECAY
        self.min_exploration_rate = Config.MIN_EXPLORATION_RATE
        
        self.q_table = np.random.uniform(
            low=-0.1, 
            high=0.1, 
            size=(state_space_size[0], state_space_size[1], action_space_size)
        )
        
        self.episode_rewards = []
        self.episode_steps = []
        self.exploration_rates = []
    
    def get_action(self, state):
        if random.random() < self.exploration_rate:
            return random.randint(0, self.action_space_size - 1)
        else:
            state_idx = self._state_to_index(state)
            return np.argmax(self.q_table[state_idx])
    
    def _state_to_index(self, state):
        return (state[0], state[1])
    
    def learn(self, state, action, reward, next_state, done):
        state_idx = self._state_to_index(state)
        next_state_idx = self._state_to_index(next_state)
        
        current_q = self.q_table[state_idx][action]
        
        if done:
            target_q = reward
        else:
            max_future_q = np.max(self.q_table[next_state_idx])
            target_q = reward + self.discount_factor * max_future_q
        
        self.q_table[state_idx][action] = current_q + self.learning_rate * (target_q - current_q)
    
    def update_exploration_rate(self):
        self.exploration_rate = max(
            self.min_exploration_rate, 
            self.exploration_rate * self.exploration_decay
        )
    
    def record_episode(self, total_reward, steps):
        self.episode_rewards.append(total_reward)
        self.episode_steps.append(steps)
        self.exploration_rates.append(self.exploration_rate)
    
    def get_best_policy(self):
        policy = {}
        for i in range(self.state_space_size[0]):
            for j in range(self.state_space_size[1]):
                best_action = np.argmax(self.q_table[i][j])
                policy[(i, j)] = best_action
        return policy
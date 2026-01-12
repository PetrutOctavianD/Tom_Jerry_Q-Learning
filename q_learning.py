import numpy as np
import time
from environment import MazeEnvironment
from agent import QLearningAgent
from config import Config

class QLearningTrainer:
    def __init__(self):
        self.env = MazeEnvironment()
        
        max_distance_y = Config.MAZE_HEIGHT - 1
        max_distance_x = Config.MAZE_WIDTH - 1
        state_space_size = (max_distance_y + 1, max_distance_x + 1)
        
        action_space_size = 4
        
        self.agent = QLearningAgent(state_space_size, action_space_size)
        self.training_stats = []
    
    def train(self, episodes=Config.EPISODES):
        start_time = time.time()
        successes = 0
        
        for episode in range(episodes):
            state = self.env.reset()
            total_reward = 0
            steps = 0
            episode_done = False
            
            while not episode_done and steps < Config.MAX_STEPS_PER_EPISODE:
                action = self.agent.get_action(state)
                
                next_state, reward, done = self.env.step(action)
                
                self.agent.learn(state, action, reward, next_state, done)
                
                state = next_state
                total_reward += reward
                steps += 1
                episode_done = done
            
            if self.env.cat_pos == self.env.mouse_pos:
                successes += 1
            
            self.agent.record_episode(total_reward, steps)
            self.agent.update_exploration_rate()
            
            self.training_stats.append({
                'episode': episode,
                'reward': total_reward,
                'steps': steps,
                'success': self.env.cat_pos == self.env.mouse_pos,
                'exploration': self.agent.exploration_rate
            })

        return self.agent
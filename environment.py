import numpy as np
import random
from config import Config

class MazeEnvironment:
    def __init__(self, width=Config.MAZE_WIDTH, height=Config.MAZE_HEIGHT):
        self.width = width
        self.height = height
        self.reset()
        
    def reset(self):
        self.maze = self._generate_simple_maze()
        
        self.cat_pos = self._get_start_position()
        self.mouse_pos = self._get_goal_position()
        
        while self.cat_pos == self.mouse_pos or self._is_wall(self.cat_pos) or self._is_wall(self.mouse_pos):
            self.cat_pos = self._get_start_position()
            self.mouse_pos = self._get_goal_position()
            
        self.steps = 0
        self.done = False
        self.total_reward = 0
        
        return self._get_state()
    
    def _generate_simple_maze(self):
        maze = np.zeros((self.height, self.width), dtype=int)
        
        for i in range(self.height):
            for j in range(self.width):
                if (i == 0 or i == self.height-1 or 
                    j == 0 or j == self.width-1):
                    if random.random() < 0.6:  
                        maze[i][j] = 1
                else:
                    if random.random() < 0.08: 
                        maze[i][j] = 1
        
        maze[1][1] = 0  
        maze[self.height-2][self.width-2] = 0  
        
        for i in range(1, self.height-1):
            for j in range(1, self.width-1):
                if maze[i][j] == 1:
                    neighbors = [
                        maze[i-1][j], maze[i+1][j],
                        maze[i][j-1], maze[i][j+1]
                    ]
                    if sum(neighbors) >= 3:  
                        maze[i][j] = 0  
        return maze
    
    def _get_start_position(self):
        return (1, 1)  
    
    def _get_goal_position(self):
        return (self.height-2, self.width-2)  
    
    def _get_state(self):
        dy = abs(self.cat_pos[0] - self.mouse_pos[0])
        dx = abs(self.cat_pos[1] - self.mouse_pos[1])
        return (dy, dx)
    
    def step(self, action):
        self.steps += 1
        
        new_cat_pos = self._move_agent(self.cat_pos, action)
        
        if self._is_wall(new_cat_pos):
            reward = Config.REWARD_WALL
            new_cat_pos = self.cat_pos 
        else:
            self.cat_pos = new_cat_pos
            reward = Config.REWARD_STEP
            
            old_distance = self._manhattan_distance(self.cat_pos, self.mouse_pos)
            new_distance = self._manhattan_distance(new_cat_pos, self.mouse_pos)
            
            if new_distance < old_distance:
                reward += Config.REWARD_CLOSER * (old_distance - new_distance)  
            elif new_distance > old_distance:
                reward -= Config.REWARD_CLOSER * 0.5  
        
        if random.random() < 0.3:  
            self._move_mouse_simple()
        
        if self.cat_pos == self.mouse_pos:
            reward = Config.REWARD_CATCH
            self.done = True
        
        if self.steps >= Config.MAX_STEPS_PER_EPISODE:
            self.done = True
            
        self.total_reward += reward
        next_state = self._get_state()
        
        return next_state, reward, self.done
    
    def _move_agent(self, pos, action):
        y, x = pos
        
        if action == 0:  
            y = max(0, y - 1)
        elif action == 1:  
            y = min(self.height - 1, y + 1)
        elif action == 2:  
            x = max(0, x - 1)
        elif action == 3:  
            x = min(self.width - 1, x + 1)
            
        return (y, x)
    
    def _move_mouse_simple(self):
        current_y, current_x = self.mouse_pos
        
        possible_moves = []
        
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)  
        
        for dy, dx in directions:
            new_y = current_y + dy
            new_x = current_x + dx
            
            if (0 <= new_y < self.height and 
                0 <= new_x < self.width and 
                self.maze[new_y][new_x] == 0):
                possible_moves.append((new_y, new_x))
                break  
        
        if possible_moves:
            self.mouse_pos = possible_moves[0]
    
    def _is_wall(self, pos):
        y, x = pos
        return self.maze[y][x] == 1
    
    def _manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
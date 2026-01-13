import pygame
import numpy as np
from config import Config

class MazeVisualizer:
    def __init__(self, env, agent):
        self.env = env
        self.agent = agent
        
        self.panel_height = 180 
        self.screen_width = Config.SCREEN_WIDTH  
        self.screen_height = Config.SCREEN_HEIGHT  
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tom & Jerry - Q-Learning")
        
        self.clock = pygame.time.Clock()
        self.small_font = pygame.font.SysFont('Arial', 16)  
        self.tiny_font = pygame.font.SysFont('Arial', 13)   
        
        self.path = []
        self.episode_count = 0
        self.running = True
        self.paused = False
        
        self.total_score = 0.0
        self.best_score = -9999.0
        self.current_episode_score = 0.0
        self.success_count = 0
        
        self.panel_y = Config.MAZE_HEIGHT * Config.CELL_SIZE
        
        col_width = self.screen_width // 3
        
        self.col1_x = 15
        self.col2_x = col_width + 15
        self.col3_x = 2 * col_width + 15
    
    def update_score(self, episode_reward, success):
        self.current_episode_score = episode_reward
        self.total_score += episode_reward
        
        if episode_reward > self.best_score:
            self.best_score = episode_reward
        
        if success:
            self.success_count += 1
    
    def draw_maze(self):
        self.screen.fill(Config.BACKGROUND)
        
        for y in range(self.env.height):
            for x in range(self.env.width):
                center_x = x * Config.CELL_SIZE + Config.CELL_SIZE // 2
                center_y = y * Config.CELL_SIZE + Config.CELL_SIZE // 2
                radius = Config.CELL_SIZE // 2.8
                
                if self.env.maze[y][x] == 1:
                    pygame.draw.circle(self.screen, Config.WALL, (center_x, center_y), radius)
                else:
                    pygame.draw.circle(self.screen, Config.EMPTY, (center_x, center_y), radius)
                    pygame.draw.circle(self.screen, Config.GRID, (center_x, center_y), radius, 2)
        
        for i, (pos_y, pos_x) in enumerate(self.path[-10:]):
            alpha = 150
            color = (*Config.PATH[:3], alpha) if len(Config.PATH) > 3 else (*Config.PATH, alpha)
            
            center_x = pos_x * Config.CELL_SIZE + Config.CELL_SIZE // 2
            center_y = pos_y * Config.CELL_SIZE + Config.CELL_SIZE // 2
            trail_radius = Config.CELL_SIZE // 8
            
            pygame.draw.circle(self.screen, color[:3], (center_x, center_y), trail_radius)
    
    def draw_agents(self):
        mouse_x, mouse_y = self.env.mouse_pos[1], self.env.mouse_pos[0]
        mouse_center_x = mouse_x * Config.CELL_SIZE + Config.CELL_SIZE // 2
        mouse_center_y = mouse_y * Config.CELL_SIZE + Config.CELL_SIZE // 2
        mouse_radius = Config.CELL_SIZE // 2.8
        
        pygame.draw.circle(self.screen, Config.MOUSE, (mouse_center_x, mouse_center_y), mouse_radius)
        
        mouse_text = self.small_font.render("J", True, (255, 255, 255))
        mouse_text_rect = mouse_text.get_rect(center=(mouse_center_x, mouse_center_y))
        self.screen.blit(mouse_text, mouse_text_rect)
        
        cat_x, cat_y = self.env.cat_pos[1], self.env.cat_pos[0]
        cat_center_x = cat_x * Config.CELL_SIZE + Config.CELL_SIZE // 2
        cat_center_y = cat_y * Config.CELL_SIZE + Config.CELL_SIZE // 2
        cat_radius = Config.CELL_SIZE // 2.8
        
        pygame.draw.circle(self.screen, Config.CAT, (cat_center_x, cat_center_y), cat_radius)
        
        cat_text = self.small_font.render("T", True, (255, 255, 255))
        cat_text_rect = cat_text.get_rect(center=(cat_center_x, cat_center_y))
        self.screen.blit(cat_text, cat_text_rect)
    
    def draw_score_panel(self):
        pygame.draw.rect(self.screen, Config.PANEL, 
                        (0, self.panel_y, self.screen_width, self.panel_height))
        
        pygame.draw.line(self.screen, (120, 120, 120), 
                        (0, self.panel_y), (self.screen_width, self.panel_y), 3)
        
        row_height = 30
        
        ep_text = self.small_font.render(f"Episod: {self.episode_count}", True, (0, 0, 150))
        self.screen.blit(ep_text, (self.col1_x, self.panel_y + 20))
        
        steps_text = self.small_font.render(f"Pasi: {self.env.steps}", True, (30, 30, 30))
        self.screen.blit(steps_text, (self.col1_x, self.panel_y + 20 + row_height))
        
        reward_text = self.small_font.render(f"Recompensa: {self.env.total_reward:.1f}", True, (30, 30, 30))
        self.screen.blit(reward_text, (self.col1_x, self.panel_y + 20 + 2*row_height))

        success_rate = (self.success_count / self.episode_count * 100) if self.episode_count > 0 else 0
        success_text = self.small_font.render(f"Succes: {success_rate:.1f}%", True, (0, 120, 0))
        self.screen.blit(success_text, (self.col2_x, self.panel_y + 20))
        
        explore_text = self.small_font.render(f"Explorare: {self.agent.exploration_rate:.3f}", True, (120, 0, 120))
        self.screen.blit(explore_text, (self.col2_x, self.panel_y + 20 + row_height))
        
        success_count_text = self.small_font.render(f"Total succes: {self.success_count}", True, (0, 100, 0))
        self.screen.blit(success_count_text, (self.col2_x, self.panel_y + 20 + 2*row_height))
        
        score_text = self.small_font.render(f"Scor episod: {self.env.total_reward:.1f}", True, (180, 0, 0))
        self.screen.blit(score_text, (self.col3_x, self.panel_y + 20))
        
        record_text = self.small_font.render(f"Record: {self.best_score:.1f}", True, (180, 140, 0))
        self.screen.blit(record_text, (self.col3_x, self.panel_y + 20 + row_height))
        
        total_text = self.small_font.render(f"Total: {self.total_score:.1f}", True, (0, 100, 180))
        self.screen.blit(total_text, (self.col3_x, self.panel_y + 20 + 2*row_height))
        
    
    def draw_pause_indicator(self):
        if self.paused:
            overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            self.screen.blit(overlay, (0, 0))
            
            pause_text = self.small_font.render("PAUZA (SPACE pentru a continua)", True, (255, 255, 100))
            text_rect = pause_text.get_rect(center=(self.screen_width//2, self.screen_height//2))
            self.screen.blit(pause_text, text_rect)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                    return False
        
        return True
    
    def update_path(self):
        self.path.append(self.env.cat_pos)
        if len(self.path) > 15:
            self.path.pop(0)
    
    def run_episode(self):
        self.env.reset()
        self.path = []
        self.episode_count += 1
        self.current_episode_score = 0.0
        
        step = 0
        episode_done = False
        
        while step < Config.MAX_STEPS_PER_EPISODE and not episode_done and self.running:
            if not self.handle_events():
                return False
            
            if not self.paused:
                state = self.env._get_state()
                action = self.agent.get_action(state)
                next_state, reward, done = self.env.step(action)
                self.agent.learn(state, action, reward, next_state, done)
                
                self.current_episode_score = self.env.total_reward
                self.update_path()
                
                step += 1
                episode_done = done
            
            self.draw_maze()
            self.draw_agents()
            self.draw_score_panel()
            self.draw_pause_indicator()
            
            pygame.display.flip()
            self.clock.tick(Config.FPS)
        
        if self.running:
            success = (self.env.cat_pos == self.env.mouse_pos)
            self.update_score(self.env.total_reward, success)
            self.show_episode_result(success)
        
        return self.running
    
    def show_episode_result(self, success):
        if success:
            result_text = f"SUCCES! Scor: {self.current_episode_score:.1f}"
            result_color = (0, 200, 0)
        else:
            result_text = f"Timp expirat. Scor: {self.current_episode_score:.1f}"
            result_color = (200, 100, 100)
        
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        result_surface = self.small_font.render(result_text, True, result_color)
        text_rect = result_surface.get_rect(center=(self.screen_width//2, self.screen_height//2 - 10))
        self.screen.blit(result_surface, text_rect)
        
        pygame.display.flip()
        pygame.time.wait(1000)
    
    def run_training_visualization(self, num_episodes=50):
        
        for episode in range(num_episodes):
            if not self.running:
                break
            if not self.run_episode():
                break
        
        self.show_final_results(num_episodes)
        pygame.quit()
    
    def show_final_results(self, num_episodes):
        print("\nREZULTATE FINALE:")
        print(f"Episoade: {self.episode_count}")
        print(f"Scor total: {self.total_score:.1f}")
        print(f"Record: {self.best_score:.1f}")
        print(f"Succesuri: {self.success_count}/{self.episode_count}")
        
        success_rate = (self.success_count / self.episode_count * 100) if self.episode_count > 0 else 0
        print(f"Rata succes: {success_rate:.1f}%")
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
            
            self.draw_maze()
            self.draw_agents()
            self.draw_score_panel()
            
            overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 60, 220))
            self.screen.blit(overlay, (0, 0))
            
            success_rate = (self.success_count / self.episode_count * 100) if self.episode_count > 0 else 0
            
            final_stats = [
                "ANTRENARE TERMINATA ",
                f"Episoade: {self.episode_count}",
                f"Scor total: {self.total_score:.1f}",
                f"Record: {self.best_score:.1f}",
                f"Succesuri: {self.success_count}/{self.episode_count}",
                f"Rata succes: {success_rate:.1f}%",
                "",
                "Apasa ESC pentru a inchide"
            ]
            
            for i, stat in enumerate(final_stats):
                if stat == "":
                    continue
                    
                if i == 0:  
                    color = (255, 255, 100)
                    font_size = self.small_font
                elif i == 2:  
                    color = (100, 255, 100)  
                    font_size = self.small_font
                elif i == 3:  
                    color = (255, 215, 0)  
                    font_size = self.small_font
                else:  
                    color = (220, 220, 255)
                    font_size = self.small_font
                
                text_surface = font_size.render(stat, True, color)
                text_rect = text_surface.get_rect(
                    center=(self.screen_width//2, 
                           self.screen_height//2 - 100 + i * 28)
                )
                self.screen.blit(text_surface, text_rect)
            
            pygame.display.flip()
            self.clock.tick(30)
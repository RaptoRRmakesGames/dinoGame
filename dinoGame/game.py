import pygame, json, sys
from time import time

from dinoGame.task_managers import TaskManager

class Game:
    
    def __init__(self):
        
        self.logs = []
        
        self.task_manager = TaskManager()
        self.clock = pygame.time.Clock()

        self.fps = 60        
        self.target_fps = 60
        
        self.last_time = time()
        
    def set_target_fps(self, fps: float):
        
        self.target_fps = fps
        
    def set_fps_cap(self, fps: float):
        
        self.fps = fps
        
    def update_perf_logs(self):
        
        self.logs.append({
            'fps':self.clock.get_fps(),
            
            
            })
        
    def get_dt(self):
        
        tn = time()
        
        dt = (tn - self.last_time ) * self.target_fps
         
        self.last_time = tn
        
        return dt 

    def get_fps(self, astype= float, round=2):
        
        return astype(round(self.clock.get_fps(), round))

    def quitprocess(self):
        
        with open('logs/perf_logs.json', 'w') as f: 
        
            json.dump(self.logs, f)
        
        sys.exit()
    
    def quit(self):
        
        self.quitprocess()
        
    def update(self):
        
        return

    def run(self):
        
        while True:
            
            self.clock.tick(self.fps)
            
            self.update()
            
            for event in pygame.event.get():
                
                if event.type == pygame.event.get():
                    
                    if event.type == pygame.QUIT():
                        
                        self.quit()
                    
                    if event.type == pygame.KEYDOWN:
                        
                        self.task_manager.run_binds(event)
                
            pygame.display.update()
            
            self.update_perf_logs()
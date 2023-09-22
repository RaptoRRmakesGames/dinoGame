import pygame , sys, json
from time import time
from pygame.locals import * 

from scripts.task_manager import TaskManager
from scripts.player import Player

class Game:
    
    def __init__(self):
        
        self._initDisplay()
        
        self._initClock()
        
        self._initBinds()
        
        self._initPerformanceLogs()
        
        self._init_world()
        
        self._init_player()
        
        self._initCamera()
        
    def _init_player(self):
        
        self.player = Player(self, (500,-50))
   
    def _init_world(self):
        from scripts.world import World
        self.world = World()

        self.world.load('world.pcl')
        
        self.world_set = self.world.as_set()
        
        self.world_surf = self.world.draw_world()

    def _initDisplay(self):
        flags = pygame.FULLSCREEN | pygame.SCALED
        
        self.zoom = 1.5
        
        self.screen = pygame.display.set_mode((960/self.zoom , 540/self.zoom), flags = flags)

    def _initCamera(self):
        self.camera_target = [0,0]
        self.scroll = [0,0]
        self.scroll_speed = 15
    
    def _initClock(self):
        self.clock = pygame.time.Clock()
        self.target_fps = 60
        self.fps = 0
        self.dt = 0
        self.last_time = time()

    def _initBinds(self):
        self.task_manager = TaskManager()
    
        self.task_manager.bind(pygame.K_ESCAPE, self.quit)

    def _initPerformanceLogs(self):
        
        self.logs = []

    def update_perf_logs(self):
        
        self.logs.append({
            'fps':self.clock.get_fps(),
            
            
            })

    def quit(self):
        
        with open('logs/perf_logs.json', 'w') as f: 
            
            json.dump(self.logs, f)
        
        sys.exit()

    def update_camera(self, dt=1):
        
        # calculate the camera's target
        target_x = self.player.ph.get_rect().centerx - self.screen.get_width() / 2
        target_y = self.player.ph.get_rect().centery- self.screen.get_height() / 2
            
        # move the camera
        self.camera_target[0] += ((target_x - self.camera_target[0]) / self.scroll_speed)  * dt
        self.camera_target[1] += ((target_y - self.camera_target[1]) / self.scroll_speed) * dt
    
        # Apply the camera target position as the scroll position
        self.scroll[0] = round(self.camera_target[0])
        self.scroll[1] = round(self.camera_target[1])

    def update(self):
        
        self.screen.fill((15,29,39))
        
        self.dt = self.get_dt()
        
        self.update_camera(self.dt)
        
        self.screen.blit(self.world_surf, (-self.scroll[0],-self.scroll[1],))
        
        self.player.render(self.screen, self.scroll)
        
        self.player.update(self.world.tiles, self.dt)

    def run(self):
        
        while True:
            
            self.clock.tick(self.fps)
            
            self.update()
            
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    
                    self.quit()
                    
                if event.type == pygame.KEYDOWN:
                    
                    self.task_manager.run_binds(event)
                    
                    
            pygame.display.update()
            
            self.update_perf_logs()

    def get_dt(self):
        
        tn = time()
        
        dt = (tn - self.last_time ) * self.target_fps
         
        self.last_time = tn
        
        return dt 
            
if __name__ =='__main__':
    game =Game()
    game.run()
import pygame, pickle
pygame.init()

from dinoGame.task_managers import TaskManager

class World:
    
    def __init__(self, tile_size_x =16, tile_size_y = 16):
        
        self.tiles = {}
        
        self.tile_size_x = tile_size_x
        self.tile_size_y = tile_size_y
        
        self.tile_imgs = self.load_tile_images()
        
    def load(self, filename):
        
        with open(f'assets/worlds/{filename}', 'rb') as f:
            
            self.tiles = pickle.load(f)
        
    def load_tile_images(self):

        tileset = pygame.image.load('assets/images/tileset/tiles.png').convert()
        
        iter = tileset.get_width() // self.tile_size_x
        
        surfs = []
        
        for i in range(iter):
            
            surf = tileset.subsurface(pygame.Rect(i * self.tile_size_x, 0, self.tile_size_x, self.tile_size_y))
            
            surf.convert_alpha()
            
            surfs.append(surf)
            
        return surfs 
        
    def add_tile(self, tile_pos , tile_tuple):
        
        self.tiles[tile_pos]= tile_tuple
        
    def as_set(self):
        
        se = set()
        
        for tile in self.tiles:
            tx, ty = map(int, tile.split(":"))
            tup = self.tiles[tile]
            se.add((*tup, (tx,ty)))
        return se
            
        
    def draw_world(self):
        
        world_surface = pygame.Surface((2400,2400)).convert_alpha()
        
        for tile in self.tiles:
            
            tile_tuple = self.tiles[tile]
            
            tile_cord_x, tile_cord_y = int(tile.split(':')[0]),int(tile.split(':')[1])
            
            cord_x, cord_y = tile_cord_x * self.tile_size_x, tile_cord_y * self.tile_size_y
            
            tile_surf = self.tile_imgs[tile_tuple[0]]
            
            world_surface.blit(tile_surf, (cord_x, cord_y))
            
        world_surface.set_colorkey((0,0,0))
            
        return world_surface
            
class LevelEditor(World):
    def __init__(self):
        super().__init__()
        
        flags = pygame.FULLSCREEN | pygame.SCALED
        
        self.zoom = 1
        self.load('world.pcl')
        
        self.brush_size = 1 
        
        self.screen = pygame.display.set_mode((960/self.zoom , 540/self.zoom), flags = flags)
        
        self.grid = self.draw_grid()
        
        self.task_manager = TaskManager()
        
        self.clock = pygame.time.Clock()
        
        self.setting = 0 
        
        self.scroll = [0,0]
        
        self.task_manager.bind(pygame.K_ESCAPE, self.quit)
        self.task_manager.bind(pygame.K_1, self.switch_setting, [0])
        self.task_manager.bind(pygame.K_2, self.switch_setting, [1])
        self.task_manager.bind(pygame.K_3, self.switch_setting, [2])
        
        self.task_manager.bind(pygame.K_c, self.set_size, [1])
        self.task_manager.bind(pygame.K_v, self.set_size, [2])
        self.task_manager.bind(pygame.K_b, self.set_size, [3])
        
        self.world = self.draw_world()
        
        self.tile_imgs = self.load_tile_images()
        
        
    def quit(self):
        
        self.save()
        
        exit()
        
    def save(self):
        
        with open('assets/worlds/world.pcl', 'wb') as f:
            
            pickle.dump(self.tiles, f)
        
    def draw_grid(self):
        
        surf = pygame.Surface((2400,2400), pygame.SRCALPHA)
        
        for i in range(150):
            for x in range(150):
                
                pygame.draw.rect(surf, (255,255,255, 50), pygame.Rect(i*16, x*16, 16,16,), 1)
                
                
        surf.set_colorkey((0,0,0))
        surf.convert_alpha()
        
        return surf 
        
    def update(self):
        
        
        self.screen.fill((8,16,32))
        
        self.scroll_camera()
        
        self.screen.blit(self.world, (-self.scroll[0], - self.scroll[1]))
        self.screen.blit(self.grid, (-self.scroll[0],-self.scroll[1]))
        
    def draw_selected(self):
        tx, ty = self.get_pos()
        
        if self.brush_size == 1:
            pygame.draw.rect(self.screen, (255,255,255), pygame.Rect((tx * 16) - self.scroll[0], (ty * 16) - self.scroll[1], 16,16), 1)
        if self.brush_size == 2:
            pygame.draw.rect(self.screen, (255,255,255), pygame.Rect((tx * 16) - self.scroll[0], (ty * 16) - self.scroll[1], 32,32), 1)
        if self.brush_size == 3:
            pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(((tx-1) * 16)- self.scroll[0], ((ty-1) * 16)- self.scroll[1], 48,48), 1)
        
    def switch_setting(self, setting):
        
        self.setting = setting 
        
    def set_size(self, size):
        
        self.brush_size = size 
    
    def scroll_camera(self):
        
        keys = pygame.key.get_pressed()
        
        self.scroll[0] += (keys[pygame.K_d] - keys[pygame.K_a] ) *1
        self.scroll[1] += (keys[pygame.K_s] - keys[pygame.K_w] ) *1
        
    def get_pos(self):
        
        diff_x, diff_y = 1920 // self.screen.get_width(), 1080 // self.screen.get_height()
        
        mouse_pos = (pygame.mouse.get_pos()[0] + self.scroll[0]) * diff_x, (pygame.mouse.get_pos()[1] + self.scroll[1]) * diff_y
        
        tile_x, tile_y = mouse_pos[0] // self.tile_size_x // 2,mouse_pos[1] // self.tile_size_y //2,
        
        return tile_x, tile_y
    
    def handle_mouse(self):
        tx, ty = self.get_pos()
        
        
        if pygame.mouse.get_pressed()[0]:
            
            tx, ty = self.get_pos()
            if self.brush_size == 1:
            
                self.add_tile(f"{tx}:{ty}", (self.setting, True))
            if self.brush_size == 2:
            
                self.add_tile(f"{tx}:{ty}", (self.setting, True))
                self.add_tile(f"{tx+1}:{ty+1}", (self.setting, True))
                self.add_tile(f"{tx+1}:{ty}", (self.setting, True))
                self.add_tile(f"{tx}:{ty+ 1}", (self.setting, True))
                
            if self.brush_size == 3:
                
                self.add_tile(f"{tx}:{ty}", (self.setting, True))
                self.add_tile(f"{tx+1}:{ty+1}", (self.setting, True))
                self.add_tile(f"{tx+1}:{ty-1}", (self.setting, True))
                self.add_tile(f"{tx-1}:{ty-1}", (self.setting, True))
                self.add_tile(f"{tx-1}:{ty+1}", (self.setting, True))
                self.add_tile(f"{tx+1}:{ty}", (self.setting, True))
                self.add_tile(f"{tx-1}:{ty}", (self.setting, True))
                self.add_tile(f"{tx}:{ty+1}", (self.setting, True))
                self.add_tile(f"{tx}:{ty-1}", (self.setting, True))
                
            
            self.world = self.draw_world()
        
        if pygame.mouse.get_pressed()[2]:
            
            if self.brush_size == 1:
                try:
                
                    del self.tiles[f"{tx}:{ty}"]
                    
                except KeyError:
                    
                    pass
            
            if self.brush_size == 2:
                
                lst = [f"{tx}:{ty}",
                    f"{tx+1}:{ty+1}",
                    f"{tx+1}:{ty}",
                    f"{tx}:{ty+ 1}",]
                
                for l in lst:
                    
                    try:
            
                        del self.tiles[l]
                
                    except KeyError:
                        
                        pass
                    
            if self.brush_size == 3:
                
                lst = [f"{tx}:{ty}",
                    f"{tx+1}:{ty+1}",
                    f"{tx+1}:{ty-1}",
                    f"{tx-1}:{ty-1}",
                    f"{tx-1}:{ty+1}",
                    f"{tx+1}:{ty}",
                    f"{tx-1}:{ty}",
                    f"{tx}:{ty+1}",
                    f"{tx}:{ty-1}",]
                
                for l in lst:
                    
                    try:
            
                        del self.tiles[l]
                
                    except KeyError:
                        
                        pass
            
            
            self.world = self.draw_world()


    def run(self):
        
        while True:
            
            self.clock.tick(0)
            
            self.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    
                    self.quit()
                    
                if event.type == pygame.KEYDOWN:
                    
                    self.task_manager.run_binds(event)
                    
            self.draw_selected()
            self.handle_mouse()
                    

                    
                    
            pygame.display.flip()
            

import pygame, os

G = 0.3

class PhysicsBody:
    
    def __init__(self, pos, size, friction=0.07):
        
        self.rect = pygame.FRect(*pos, *size)
        
        self.velocity = pygame.math.Vector2(0,0)
        
        self.fr_speed = friction
        
        self.dx,self.dy = 0,0
        
    def update_gravity(self, dt=1):
        
        self.velocity.y += G * dt

        
    def move(self, dt=1):
        
        # print(self.velocity)
        
        self.rect.x += self.velocity.x  * dt
        self.rect.y += self.velocity.y * dt
        
    def cap_vel(self):
        if self.velocity.x > self.max_x:
            
            self.velocity.x = self.max_x
            
        if self.velocity.x < -self.max_x:
            
            self.velocity.x = -self.max_x
            
        if self.velocity.y > self.max_y:
            
            self.velocity.y = self.max_y
            
        if self.velocity.y < -self.max_y:
            
            self.velocity.y = -self.max_y
    
    def friction(self, dt=1):
        
        self.dx,self.dy = self.velocity.x, self.velocity.y
        
        if self.set_max_bool:
            self.cap_vel()
        
        self.velocity.x = self.velocity.move_towards((0,0), self.fr_speed * dt).x
        # self.velocity.y = self.velocity.move_towards((0,0), self.fr_speed).y
        
    def applyForce(self, vec):
        vec = pygame.math.Vector2(vec)
        
        self.velocity.x += vec.x 
        self.velocity.y += vec.y
        
    def set_max_vel(self, num_x, num_y=None):
        
        if not num_y:
            num_y = num_x 
            
        self.max_x = num_x 
        self.max_y = num_y
        
        self.set_max_bool = True
    
    def get_rect(self):
        
        return self.rect 
    
    def get_pos(self):
        
        return self.rect.topleft  
    
class Collider:
    
    def __init__(self, parent):
        
        self.parent = parent
        self.on_ground = False
        
    def check_collide_world(self, tiles):
        
        self.on_ground = False
        
        ph = self.parent.ph
        
        ptx, pty = ph.get_rect().x // 16, ph.get_rect().y // 16
        
        if isinstance(tiles, dict):

            
            for tile in tiles:
                
                tx, ty = map(int, tile.split(":"))
                
                if abs(ptx - tx) + abs(pty - ty) < 10:
                    
                
                    x, y = tx*16, ty *16
                    
                    tile_rect = pygame.Rect(x,y, 16,16)

                    if tile_rect.colliderect(ph.get_rect().move(ph.dx, 0)):
                        
                        ph.dx = 0 
                        
                        if ph.velocity.x > 0:
                            
                            ph.get_rect().right = tile_rect.left
                            
                        if ph.velocity.x < 0:
                            
                            ph.get_rect().left = tile_rect.right
                            
                        
                        ph.velocity.x = 0
                    
                    if tile_rect.colliderect(ph.get_rect().move(0, ph.dy)):
                        
                        ph.dy = 0 
                        
                        if ph.velocity.y > 0:
                            self.on_ground = True
                            self.parent.jumps = 2
                            
                            ph.get_rect().bottom = tile_rect.top
                        if ph.velocity.y < 0:
                            
                            ph.get_rect().top = tile_rect.bottom
                            
                        
                        ph.velocity.y = 0
        elif isinstance(tiles, set):
            
            for tile in tiles:
                
                tx, ty = tile[2]
                
                if abs(ptx - tx) + abs(pty - ty) < 10:
                    
                
                    x, y = tx*16, ty *16
                    
                    tile_rect = pygame.Rect(x,y, 16,16)

                    if tile_rect.colliderect(ph.get_rect().move(ph.dx, 0)):
                        
                        ph.dx = 0 
                        
                        if ph.velocity.x > 0:
                            
                            ph.get_rect().right = tile_rect.left
                            
                        if ph.velocity.x < 0:
                            
                            ph.get_rect().left = tile_rect.right
                            
                        
                        ph.velocity.x = 0
                    
                    if tile_rect.colliderect(ph.get_rect().move(0, ph.dy)):
                        
                        ph.dy = 0 
                        
                        if ph.velocity.y > 0:
                            self.on_ground = True
                            self.parent.jumps = 2
                            
                            ph.get_rect().bottom = tile_rect.top
                        if ph.velocity.y < 0:
                            
                            ph.get_rect().top = tile_rect.bottom
                            
                        
                        ph.velocity.y = 0
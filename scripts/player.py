import pygame

from scripts.classes import PhysicsBody, Collider, InputController, Animator

class Player:
    
    def __init__(self, game, pos):
        
        self.game = game
        
        self.anm = Animator()
        
        self.anm.create_all_anims('assets/images/player/', [150,150,50,150,150,150,150])
        
        self.anm.set_anim('idle')
        
        self.image = self.anm.get_image()
        
        img_rect = self.image.get_rect(topleft=pos)
        
        self.ph = PhysicsBody(pos, (img_rect.width, img_rect.height))
        self.ph.set_max_vel(2, 12)
        
        self.sprint_multi = 2
        
        self.cl = Collider(self)
        
        self.inputs = InputController()
        
        self.inputs.set_listener(pygame.K_SPACE, 'jump')
        self.inputs.set_listener(pygame.K_a, 'left')
        self.inputs.set_listener(pygame.K_d, 'right')
        self.inputs.set_listener(pygame.K_LSHIFT, 'sprint')
        
        self.jumps = 2
        self.jumped = False 
        
    def render(self, display, offset):
        
        render_rect = pygame.FRect(self.ph.get_pos()[0] - offset[0],self.ph.get_pos()[1] - offset[1], self.ph.get_rect().width,self.ph.get_rect().height )
         
        display.blit(self.anm.get_image(), render_rect)
        # pygame.draw.rect(display, (255,255,255), render_rect)
        
    def update(self, tiles, dt=1):
        
        self.handle_animations()
        
        self.anm.update_anim()
        
        self.ph.update_gravity(dt)
        
        if self.inputs.down('jump') and (self.cl.on_ground or self.jumps > 0 ) and (not self.jumped or self.cl.on_ground):
            self.jumped = True
            self.ph.velocity.y = -6 - (self.jumps * 0.5)
            
            self.jumps -= 1
            
        if self.jumped:
            
            if not self.inputs.down('jump'):
                
                self.jumped = False
                
        
        self.ph.applyForce((
            ((self.inputs.down('right') - self.inputs.down('left') )* 0.3) * ( max(1, self.inputs.down('sprint') * self.sprint_multi))  , 0) 
                           )
        
        self.ph.set_max_vel(2* max(1, self.inputs.down('sprint') * self.sprint_multi), 12)
        

        
        self.ph.friction(dt)
        
    
        self.cl.check_collide_world(self.game.world_set)
        
        self.ph.move(dt)
        
    def handle_animations(self):
        pass
import pygame, os


class Animation:
    
    def __init__(self, image_list):
        
        self.images = image_list
        
        self.index = 0
        self.max_index = len(image_list)-1
        
        self.next_anim = pygame.time.get_ticks() + 150
        
        self.frame_time = 150
        
    def update(self):
        
        tn = pygame.time.get_ticks()
        
        if tn > self.next_anim:
            
            self.index += 1
            
            if self.index > self.max_index:
                
                self.index = 0
            
            self.next_anim=  tn + self.frame_time
        
    def set_frame_time(self, time):
        
        self.frame_time = time
        
    def get_image(self):
        
        return self.images[self.index]
        
                
class Animator:
    
    def __init__(self):
                   
        self.animations = {} 
        self.selected_anim = None 
        
    def __str__(self) :
        return str(self.animations)
    
    def create_animations(self, anim_name, img_folder, frame_time=150):
        
        imgs = []
        
        for fn in os.listdir(img_folder):
            
            img = pygame.image.load(os.path.join(img_folder, fn))
            
            if img is not None:
                
                imgs.append(img)
                
        self.animations[anim_name] = Animation(imgs)
        self.animations[anim_name].set_frame_time(frame_time)
        
    def create_spritesheet_anim(self, anim_name, img_sheet,single_x, frame_time=150):
        
        img = pygame.image.load(img_sheet)
        
        iters = img.get_width()//single_x
        
        imgs = []
        
        for i in range(iters):
            
            sub = img.subsurface(pygame.Rect(single_x * i, 0, single_x, img.get_height()))
            imgs.append(sub)
            
        self.animations[anim_name] = Animation(imgs)
        self.animations[anim_name].set_frame_time(frame_time)
        
    def anim_done(self):
        
        return self.selected_anim.index == self.selected_anim.max_index 
        
        
    def create_all_anims(self,folder_path, fr_times):
        
        for x, fn in enumerate(os.listdir(folder_path)):
            
            self.create_animations(fn, os.path.join(folder_path, fn), fr_times[x])
            
    def create_all_anims_spritesheet(self, folder_path, fr_times):
        
        for x, fn in enumerate(os.listdir(folder_path)):
            
            self.create_spritesheet_anim(fn, os.path.join(folder_path, fn), fr_times[x])
            
            
    def set_anim(self, anim_name):
        
        self.selected_anim = self.animations[anim_name]
        
        self.selected_anim.index = 0 
        self.selected_anim.next_anim = pygame.time.get_ticks() + self.selected_anim.frame_time
        
    def set_anim_norefresh(self, anim_name):
        self.selected_anim = self.animations[anim_name]
        
    def get_image(self):
        
        if self.selected_anim is not None:
            return self.selected_anim.get_image()
        
        return None
        
    def update_anim(self):
        
        if self.selected_anim is not None:
            
            self.selected_anim.update()
            
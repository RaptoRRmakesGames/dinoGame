
import pygame

class TaskManager:
    
    def __init__(self):
        
        self.binds = []
        
    def bind(self, key, function, args = []):
        
        self.binds.append((key, function, args))
        
    def run_binds(self, event):
        
        for bind in self.binds:
                        
            if event.key == bind[0]:
                
                bind[1](*bind[2])
                
class InputController:
    
    def __init__(self):
        
        self.inputs = {}
        
    def set_listener(self, key, nick):
        
        self.inputs[nick]  = key
        
        
    def down(self, nick):
        
        if pygame.key.get_pressed()[self.inputs[nick]]:
            
            return True
        
        return False
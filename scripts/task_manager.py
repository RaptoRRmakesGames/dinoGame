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
                
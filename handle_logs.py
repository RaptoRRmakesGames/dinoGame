import json

with open('logs/perf_logs.json') as f:
    
    dic = json.load(f)
    
    
ch = input('which collumn do u want to see?\n')

sum = 0
if ch == 'fps':
    
    for log in dic: 
        
        sum += log['fps']
        
        
print(sum/len(dic))
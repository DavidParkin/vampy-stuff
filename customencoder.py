from datetime import datetime
 
import json
import numpy 
class MyCustomEncoder(json.JSONEncoder):
 
     def default(self, o):
         print("Start")
         print(type(o))
         print(o)
         if isinstance(o, vampyhost.RealTime):
             print("Is old realtime") 
             b = o.values()
             #return {'__realtime__': o.values}
             return {'__realtime__': list(b)}
         if isinstance(o, numpy.ndarray):
             print("Is numpy")
             return {'__ndarray__': o[0]}
         if isinstance(o, numpy.float32):
             print ("Is float")
             return {'__float32__': o.tolist()} 
         print("Is not realtime")
         print(type(o)) 
         print(o)
         print("CLASS")
         print(o.__class__.__name__)       
         #return {'__{}__'.format(o.__class__.__name__): o.__dict__}
         return json.JSONEncoder.default(self, o)


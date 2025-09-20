import json
import os

class MergeIntents:
    def __init__(self, folder_path):
        self.intents = {"intents":[]}
        self.folder_path = folder_path
    
    def MergeFiles(self):
        self.files = os.listdir(self.folder_path)
        
        for file in self.files:
            if file.endswith('.json'):
                file_path = os.path.join(self.folder_path, file)
                
                with open(file_path, 'r') as f:
                    intents = json.loads(f.read())
                    
                for i in intents['intents']:
                    temp = {
                            "tag":i['tag'], 
                            "patterns":i['patterns'], 
                            "responses":i['responses'],
                            "context":[""]
                           }
                    self.intents['intents'].append(temp)
        
        print("Files Merged Successfully")
    
    def save_merged_file(self,output="merged_intent.json"):
        
        with open(output, 'w') as f:
            json.dump(self.intents, f, indent=4)
        
        print("Merged File Saved Successfully")
        

merger = MergeIntents('data/intents')
merger.MergeFiles()
merger.save_merged_file()
            
            
        
        
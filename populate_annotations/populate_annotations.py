import json
import sys

sys.path.insert(0, "..")
from annotation_generate.annotation_generate import AnnotationGeneration

'''
Create a class to populate the codebase json with annotations
- input: 
    - codebase model json file
- output:
    - modified json file with updated annotation fields
'''

class PopulateAnnotations:
    def __init__(self, model_file_path):
        self.file_path = model_file_path
        self.annotator = AnnotationGeneration()
        self.model = self.load_model()
    
    def load_model(self):
        d = {}
        with open(self.file_path) as json_data:
            d = json.load(json_data)
        return d
    
    def annotate(self, content_str):
        formated_str = content_str.replace("\n", "") # remove newline characters
        output = self.annotator.snippet_summary(formated_str)
        # output = "test"
        return output
    
    def populate(self):
        self._populate(self.model)
        
    def _populate(self, model):
        if model["type"] == "file":
            if model["content"] not in ["n/a", ""]:
                annotation = self.annotate(model["content"])
                model["annotation"] = annotation 
                return model  
        else:
            for child in model["children"]:
                self._populate(child)
    
    def save_json(self):
        save_file = open(self.file_path, 'w')
        json.dump(self.model, save_file, indent=4)
        save_file.close()
        print(f"Codebase model updated with annotations and saved: {self.file_path}")
        return self.model

class TestPopulateAnnotations:
    def __init__(self):
        self.test_json_file = "/Users/trav/Documents/projects/codesense/populate_annotations/test_codebase.json"
        self.populator = PopulateAnnotations(self.test_json_file)
        
    def test_populate_annotations(self):
        print("Testing annotation population")
        self.populator.populate()
        self.populator.save_json()

if __name__ == "__main__":
    testPopulateAnnotations = TestPopulateAnnotations()
    testPopulateAnnotations.test_populate_annotations()

                
        

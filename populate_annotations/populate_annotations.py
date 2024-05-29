import os
import sys

sys.path.insert(0, "..")
from annotation_generate.annotation_generate import AnnotationGeneration
from utilities.utility import file_to_string, obj_to_json, json_to_obj

'''
Create a class to populate the codebase json with annotations
- input: 
    - codebase model object
- output:
    - codebase model object with updated annotation fields
'''

class PopulateAnnotations:
    def __init__(self, model_obj, ignore_paths):
        #ignore_paths could be a txt file or a json object containing file_paths to ignore
        self.annotator = AnnotationGeneration()
        self.model = model_obj
        self.ignore_list = ignore_paths
    
    def annotate(self, content_str):
        formated_str = content_str.replace("\n", "") # remove newline characters
        output = self.annotator.snippet_summary(formated_str) # comment this out to stub API call for testing purposes
        # output = "test"
        return output
    
    def populate_model(self):
        self._populate(self.model, self.model["name"])
        return self.model
        
    def _populate(self, model, cur_path):
        if model["type"] == "file":
            if model["content"] not in ["n/a", ""]:
                annotation = self.annotate(model["content"])
                model["annotation"] = annotation 
                return model  
        else:
            for child in model["children"]:
                #build path string of traversal
                new_path = os.path.join(cur_path, child["name"])
                if new_path not in self.ignore_list:
                    self._populate(child, new_path)

class TestPopulateAnnotations:
    def __init__(self):
        self.test_model = json_to_obj("test_github_codebase.json") 
        self.test_ignore_file = "ignore.txt"
        self.populator = PopulateAnnotations(self.test_model, self.test_ignore_file)
        
    def test_populate_annotations(self):
        print("Testing annotation population")
        updated_model = self.populator.populate_model()
        obj_to_json("./", "test", updated_model)
        assert type(updated_model) == dict
    
        

if __name__ == "__main__":
    testPopulateAnnotations = TestPopulateAnnotations()
    testPopulateAnnotations.test_populate_annotations()

                
        

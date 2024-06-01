import os
import threading
from queue import Queue 
import sys

sys.path.insert(0, "..")
from src.annotation_generate.annotation_generate import AnnotationGeneration
from src.utilities.utility import file_to_string, obj_to_json, json_to_obj

'''
Create a class to populate the codebase json with annotations in a multithreaded manner
- input: 
    - codebase model object
- output:
    - codebase model object with updated annotation fields
'''

class BatchPopulateAnnotations:
    def __init__(self, model_obj, ignore_paths):
        self.threads = []
        self.max_threads = 5
        self.q = Queue(maxsize=0)
        self.annotator = AnnotationGeneration()
        self.model = model_obj
        self.ignore_list = ignore_paths
        self.files_to_annotate = []
        self.annotation_map = {}
    
    def get_files_to_annotate(self):
        self._get_files_to_annotate(self.model)
        return self.files_to_annotate
    
    def _get_files_to_annotate(self, model):
        if model["type"] == "file":
            if model["content"] not in ["n/a", ""]:
                self.files_to_annotate.append(model)
                return model 
        else:
            for child in model["children"]:
                if child["path"] not in self.ignore_list:
                    self._get_files_to_annotate(child)
    
    def annotate(self, file_model):
        content_str = file_model["content"]
        formated_str = content_str.replace("\n", "") # remove newline characters
        annotation = self.annotator.run(formated_str) # comment this out to stub API call for testing purposes
        # annotation = "test"
        path = file_model["path"]
        self.q.put((path, annotation))
    
    def batch_annotate(self):
        self.get_files_to_annotate()
        for file in self.files_to_annotate:
            self.threads.append(threading.Thread(
                target=self.annotate, args=(file, )))
        
        if len(self.threads) > self.max_threads:
            self._run_multi_pool()
        else:
            self._run_single_pool()
        return self._build_result()
    
    def _run_single_pool(self):
        for x in self.threads:
            x.start()
        for x in self.threads:
            x.join()

    def _run_multi_pool(self):
        for i in range(0, len(self.threads), self.max_threads):
            pool = self.threads[i: i+self.max_threads]
            for j in pool:
                j.start()
            for j in pool:
                j.join()
    
    def _build_result(self):
        while not self.q.empty():
            entry = self.q.get()
            path = entry[0]
            annotation = entry[1]
            self.annotation_map[path] = annotation
        self.populate()
        return self.model
    
    def populate(self):
        self._populate(self.model)
    
    def _populate(self, model):
        if model["type"] == "file":
            if model["content"] not in ["n/a", ""]:
                path = model["path"]
                model["annotation"] = self.annotation_map[path]
                return model
        else:
            for child in model["children"]:
                if child["path"] not in self.ignore_list:
                    self._populate(child)
                
        
class TestBatchPopulateAnnotations:
    def __init__(self):
        self.test_model = json_to_obj("test_github_codebase.json") 
        self.test_ignore_files = [
            "codesense/keyword_extract",
            "codesense/extras/codebase_extraction/codebase.json",
            "codesense/README.md"
        ]
        self.populator = BatchPopulateAnnotations(self.test_model, self.test_ignore_files)    
    
    def test_batch_populate(self):
        print("Testing batch annotation population")
        updated_model = self.populator.batch_annotate()
        obj_to_json("./", "test_batch", updated_model)
        assert type(updated_model) == dict

if __name__ == "__main__":
    testBatchPopulateAnnotations = TestBatchPopulateAnnotations()
    testBatchPopulateAnnotations.test_batch_populate()
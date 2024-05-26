import json
import sys

sys.path.insert(0, "..")
from keyword_extract.keyword_extract import KeywordExtract

'''
Create a class to populate the codebase json with keywords
- input: 
    - codebase model json file
- output:
    - modified json file with updated annotation fields
'''

class PopulateKeywords:
    def __init__(self, model_file_path):
        self.file_path = model_file_path
        self.model = self.load_model()
    
    def load_model(self):
        d = {}
        with open(self.file_path) as json_data:
            d = json.load(json_data)
        return d
    
    def extractKeywords(self, content_str):
        formated_str = content_str.replace("\n", "") # remove newline characters
        extractor = KeywordExtract()
        output = extractor.extract(formated_str)
        # output = "test"
        return output
    
    def populate(self):
        self._populate(self.model)
        
    def _populate(self, model):
        if model["type"] == "file":
            annotation = model["annotation"]
            keywords = self.extractKeywords(annotation)
            model['keywords'] = keywords
            return model  
        else:
            for child in model["children"]:
                self._populate(child)
    
    def save_json(self):
        save_file = open(self.file_path, 'w')
        json.dump(self.model, save_file, indent=4)
        save_file.close()
        print(f"Codebase model updated with keywords and saved: {self.file_path}")
        return self.model
    
class TestPopulateKeyWords:
    def __init__(self):
        self.test_json_file = "/Users/derrickratnaharan/Documents/CodeSense/codesense/populate_keywords/test_codebase.json"
        self.populator = PopulateKeywords(self.test_json_file)

    def test_populate_keywords(self):
        print("Testing annotation population")
        self.populator.populate()
        self.populator.save_json()

if __name__ == "__main__":
    testPopulateKeyWords = TestPopulateKeyWords()
    testPopulateKeyWords.test_populate_keywords()
    
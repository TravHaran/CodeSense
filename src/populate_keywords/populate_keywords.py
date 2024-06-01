import sys

sys.path.insert(0, "..")
from src.keyword_extract.keyword_extract import KeywordExtract
from src.utilities.utility import obj_to_json, json_to_obj

'''
Create a class to populate the codebase json with keywords
- input: 
    - codebase model object
- output:
    - codebase model object with updated keywords fields
'''

class PopulateKeywords:
    def __init__(self, model_obj):
        self.model = model_obj
    
    def extractKeywords(self, content_str):
        formated_str = content_str.replace("\n", "") # remove newline characters
        extractor = KeywordExtract()
        output = extractor.extract(formated_str)
        # output = "test"
        return output
    
    def populate_model(self):
        self._populate(self.model)
        return self.model
        
    def _populate(self, model):
        if model["type"] == "file":
            annotation = model["annotation"]
            content = model["content"]
            annotation_keywords = self.extractKeywords(annotation)
            content_keywords = self.extractKeywords(content)
            model['keywords'] = annotation_keywords + content_keywords
            return model  
        else:
            for child in model["children"]:
                self._populate(child)
    
    
class TestPopulateKeyWords:
    def __init__(self):
        self.test_model = json_to_obj("test_codebase_original.json")
        self.populator = PopulateKeywords(self.test_model)

    def test_populate_keywords(self):
        print("Testing annotation population")
        updated_model = self.populator.populate_model()
        obj_to_json("./", "test", updated_model)
        assert type(updated_model) == dict

if __name__ == "__main__":
    testPopulateKeyWords = TestPopulateKeyWords()
    testPopulateKeyWords.test_populate_keywords()
    
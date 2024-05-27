import json
import os

'''
Create a utilty class that contains useful functions that can be used across multiple classes
'''

class Utility:
    def obj_to_json(self, output_path, filename, obj):
        # makesure filename doesn't have .json extension
        # makesure output_path has trailing backslash
        output_file_path = os.path.join(output_path, f"{filename}.json")
        save_file = open(output_file_path, 'w')
        json.dump(obj, save_file, indent=4)
        save_file.close()
        print(f"json file saved: {output_file_path}")
        # return output file path for debugging purposes
        return output_file_path
    
    def json_to_obj(self, json_file_path):
        d = {}
        with open(json_file_path) as json_data:
            d = json.load(json_data)
        return d

class TestUtility:
    def __init__(self):
        self.test_json_file = "test.json"
        
    
    def test_json_to_obj(self):
        utility = Utility()
        test_obj = utility.json_to_obj(self.test_json_file)
        assert test_obj["data"] == "test"
    
    def test_obj_to_json(self):
        utility = Utility()
        # load object & modify it
        test_obj = utility.json_to_obj(self.test_json_file)
        test_obj["data"] = "test2"
        # write object
        utility.obj_to_json("./", "test2", test_obj)
        # verify if object was written correctly
        assert utility.json_to_obj("test2.json")["data"] == "test2"
        
if __name__ == "__main__":
    testUtility = TestUtility()
    testUtility.test_json_to_obj()
    testUtility.test_obj_to_json()
    
    
    
        
    


import os 
import json

'''
Create a class to extract a model of a codebase as a tree
- input: local directory path as a string
- output: 
    - json file containing tree structure of directory
    - at leaf nodes store content of file as a string (if it's content is readable)
'''

class CodebaseExtract:
    def __init__(self, path):
        # Initialize the output dictionary model with folder contents
        # name, type, and empty list for children
        self.path = path
        self.model = {}
        
    
    def file_to_string(self, file_path): # save file content as string
        with open(file_path, 'r') as file:
            file_content = file.read()
        file.close()
        return file_content
    
    def extract(self, path): # extracts a directory as a json object
        model = {'name': os.path.basename(path),
              'type': 'folder', 'children': []}
        # Check if the path is a directory
        if not os.path.isdir(path):
            return model
        
        # Iterate over the entries in the directory
        for entry in os.listdir(path):
            if not entry.startswith('.'): # ignore hidden folders & files
                # Create the fill path for current entry
                entry_path = os.path.join(path, entry)
                # if the entry is a directory, recursively call the function
                if os.path.isdir(entry_path):
                    model['children'].append(self.extract(entry_path))
                # if the entry is a file, create a dictionary with name and type
                else:
                    content = ""
                    # save file content as string
                    try:
                        content = self.file_to_string(entry_path)
                    except OSError:
                        content = "n/a"
                    model['children'].append({'name': entry, 'type': 'file', 'content': content})
        return model
    
    def model_to_str(self): # convert codebase json to string
        output_str = json.dumps(self.model, indent=4)
        return output_str
    
    def save_model_json(self, file_name): # codebase model json file
        save_file = open(f"{file_name}.json", 'w')
        self.model = self.extract(self.path)
        json.dump(self.model, save_file, indent=4)
        save_file.close()
        print(f"Codebase model saved as {file_name}")
        return self.model
        
        

class TestCodebaseExtract:
    def __init__(self):
        self.test_path = "/Users/trav/Documents/projects/codesense"
        self.extractor = CodebaseExtract(self.test_path)
        print("Testing Codebase Extractor...\n")
    
    def test_extract_codebase(self):
        print("Testing codebase extraction of current project directory...\n")
        output = self.extractor.save_model_json("test_codebase")
        # model_str = self.extractor.model_to_str()
        # print(f"Codebase model: {model_str}")
        assert type(output) == dict

if __name__ == "__main__":
    testCodebaseExtract = TestCodebaseExtract()
    testCodebaseExtract.test_extract_codebase()

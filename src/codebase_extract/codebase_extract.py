import os
import sys
sys.path.insert(0, "..")

from src.utilities.utility import obj_to_json, file_to_string

'''
Create a class to extract a model of a codebase as a tree
- input: local directory path as a string
- output: 
    - object containing tree structure of directory
    - at leaf nodes store content of file as a string (if it's content is readable)
'''


class CodebaseExtract:
    def __init__(self, path):
        # Initialize the output dictionary model with folder contents
        # name, type, keywords, and empty list for children
        self.path = path
        self.model = {}
    
    def get_model(self):
        self.model = self._build_model(self.path)
        return self.model

    def _build_model(self, path):  # extracts a directory as a json object
        absolute_cur_path = os.path.abspath(path)
        model = {'name': os.path.basename(path), 'path': absolute_cur_path,
                 'type': 'folder', 'keywords': [], 'children': []}
        # Check if the path is a directory
        if not os.path.isdir(path):
            return model
        # Iterate over the entries in the directory
        for entry in os.listdir(path):
            if not entry.startswith('.'): # ignore hidden folders & files
                # Create the file path for current entry
                entry_path = os.path.join(path, entry)
                # if the entry is a directory, recursively call the function
                if os.path.isdir(entry_path):
                    model['children'].append(self._build_model(entry_path))
                # if the entry is a file, create a dictionary with name and type, keywords, annotation, and content
                else:
                    content = ""
                    # save file content as string
                    try:
                        content = file_to_string(entry_path)
                    except Exception: # handle unreadable file content
                        content = "n/a"
                    absolute_entry_path = os.path.abspath(entry_path)
                    model['children'].append({'name': entry, 'path': absolute_entry_path, 'type': 'file', 'keywords': [
                    ], 'annotation': "", 'content': content})
        return model


class TestCodebaseExtract:
    def __init__(self):
        self.test_path = "../../codesense"
        self.extractor = CodebaseExtract(self.test_path)
        print("Testing Codebase Extractor...\n")

    def test_extract_codebase(self):
        print("Testing codebase extraction of current project directory...\n")
        output = self.extractor.get_model()
        obj_to_json("./", "test_codebase", output)
        assert type(output) == dict


if __name__ == "__main__":
    testCodebaseExtract = TestCodebaseExtract()
    testCodebaseExtract.test_extract_codebase()

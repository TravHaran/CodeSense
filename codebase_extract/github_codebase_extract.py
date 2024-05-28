import sys
import os
import base64
from urllib.parse import urlparse
from dotenv import load_dotenv
import requests

sys.path.insert(0, "..")

from utilities.utility import obj_to_json

class CodeBaseExtractGithub:
    def __init__(self, github_repo):
        load_dotenv()
        self.token = os.getenv('GITHUB_API_KEY') # make sure .env file contains api key
        # ex: https://github.com/TravHaran/codesense
        self.owner, self.repo_name = self.extract_owner_and_repo(github_repo)
        self.model = {}
    
    def extract_owner_and_repo(self, url):
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.strip('/').split('/')
        
        if len(path_parts) >= 2:
            owner = path_parts[0]
            repo_name = path_parts[1]
            return owner, repo_name
        else:
            raise ValueError("Invalid GitHub URL format")
    
    def get_content(self, path):
        headers = {"Authorization" : "token {}".format(self.token)}
        url = f"https://api.github.com/repos/{self.owner}/{self.repo_name}/contents/{path}"
        content = requests.get(url, headers=headers)
        return content.json()
    
    def content_is_dir(self, content):
        return type(content) == list
     
    def get_model(self):
        path_content = self.get_content("")
        self.model = self._build_model("", path_content)
        return self.model
    
    def _build_model(self, path, content):
        print(path)
        model = {'name': os.path.basename(path),
                 'type': 'folder', 'keywords': [], 'children': []}
        # Check if the path is a directory
        if not self.content_is_dir(content):
            return model
        # Iterate over the entries in the directory
        for entry in content:
            name = entry["name"]
            if not name.startswith('.'): # ignore hidden folders and files
                # Create the file path for current entry
                entry_path = os.path.join(path, name)
                # if the entry is a directory, recursively call the function
                entry_content = self.get_content(entry_path)
                if self.content_is_dir(entry_content):
                    model['children'].append(self._build_model(entry_path, entry_content))
                # if the entry is a file, create a dictionary with name and type, keywords, annotation, and content
                else:
                    content = ""
                    # the file content is from the api response is encoded in base64
                    try:
                        content = base64.b64decode(entry_content["content"]).decode('utf-8')
                        # content = entry_content["content"]
                    except Exception: # handle decode errors
                        content = "n/a"
                    model['children'].append({'name': name, 'type': 'file', 'keywords': [
                    ], 'annotation': "", 'content': content})
        return model
                        

class TestCodebaseExtractGithub:
    def __init__(self):
        self.test_github_repo = "https://github.com/TravHaran/codesense"      
        self.extractor = CodeBaseExtractGithub(self.test_github_repo)
        print("Testing Github Codebase Extractor...\n")
    
    def test_extract_codebase(self):
        print(f"Testing codebase extraction of {self.test_github_repo}\n")
        output = self.extractor.get_model()
        obj_to_json("./", "test_github_codebase", output)
        assert type(output) == dict
        
if __name__ == "__main__":
    testCodebaseExtractGithub = TestCodebaseExtractGithub()
    testCodebaseExtractGithub.test_extract_codebase()     


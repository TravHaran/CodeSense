import requests
import sys 

sys.path.insert(0, "..")
from utilities.utility import obj_to_json, json_to_obj

class TestAPI:
    def __init__(self):
        self.url = "http://127.0.0.1:8000"
        self.test_model_request = json_to_obj('test_files/test_model_request.json')
        self.test_batch_model_request = json_to_obj('test_files/test_batch_model_request.json')
        self.test_query_request = json_to_obj('test_files/test_query_request.json')
        self.test_search_request = json_to_obj('test_files/test_search_request.json')
        self.test_batch_query_request = json_to_obj('test_files/test_batch_query_request.json')
        
    def test_model(self):
        print("TESTING ENDPOINT: /model\n")
        print(f"REQUEST: \n{self.test_model_request}\n")
        response = requests.post(url=f"{self.url}/model", json=self.test_model_request).json()
        print("RESPONSE:\n")
        print(response)
        print("\n")
        obj_to_json('test_files', 'test_model_response', response)
        print("RESULT SAVED\n")
    
    def test_batch_model(self):
        print("TESTING ENDPOINT: /batchModel\n")
        response = requests.post(url=f"{self.url}/batchModel", json=self.test_batch_model_request).json()
        print("RESPONSE:\n")
        print(response)
        print("\n")
        obj_to_json('test_files', 'test_batch_model_response', response)
        print("RESULT SAVED\n")
    
    def test_search(self):
        print("TESTING ENDPOINT: /search\n")
        response = requests.get(url=f"{self.url}/search", json=self.test_search_request).json()
        print("RESPONSE:\n")
        print(response)
        print("\n")
        obj_to_json('test_files', 'test_search_response', response)
        print("RESULT SAVED\n")
    
    def test_query(self):
        print("TESTING ENDPOINT: /query\n")
        response = requests.get(url=f"{self.url}/query", json=self.test_query_request).json()
        print("RESPONSE:\n")
        print(response)
        print("\n")
        obj_to_json('test_files', 'test_query_response', response)
        print("RESULT SAVED\n")
    
    def test_batch_query(self):
        print("TESTING ENDPOINT: /batchQuery\n")
        response = requests.get(url=f"{self.url}/batchQuery", json=self.test_batch_query_request).json()
        print("RESPONSE:\n")
        print(response)
        print("\n")
        obj_to_json('test_files', 'test_batch_query_response', response)
        print("RESULT SAVED\n")

if __name__ == "__main__":
    testAPI = TestAPI()
    # testAPI.test_model()
    # testAPI.test_batch_model()
    # testAPI.test_query()
    # testAPI.test_batch_query()
    testAPI.test_search()
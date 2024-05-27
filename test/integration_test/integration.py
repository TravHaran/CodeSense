import sys


sys.path.insert(0, "../..")
from codebase_extract.codebase_extract import CodebaseExtract
from populate_annotations.populate_annotations import PopulateAnnotations
from populate_keywords.populate_keywords import PopulateKeywords
from keyword_extract.keyword_extract import KeywordExtract
from tree_traverse.tree_traverse import TraverseCodebase
from question_answering.question_answer import QueryAnswer
from utilities.utility import obj_to_json

'''
Create a class that can run a full integration test of codesense
- input: Question as a string
- output: Answer as a string
'''

class Integration:
    def __init__(self, code_base_dir, ignore_paths_file):
        self.path = code_base_dir
        self.ignore_paths_file = ignore_paths_file
        self.code_base_model = {}
        self.search_result = {}
    
    def model_codebase(self):
        # Extract Codebase
        codebase_extractor = CodebaseExtract(self.path)
        self.code_base_model = codebase_extractor.get_model()
        # Populate Annotations
        populate_annotations = PopulateAnnotations(self.code_base_model, self.ignore_paths_file)
        self.code_base_model = populate_annotations.populate_model()
        # Populate Keywords
        populate_keywords = PopulateKeywords(self.code_base_model)
        self.code_base_model = populate_keywords.populate_model()
        obj_to_json("./", "codebase", self.code_base_model)

    def query(self, question):
        # Extract Keywords
        extract_keywords = KeywordExtract()
        query_keywords = extract_keywords.extract(question)
        # Traverse Tree
        traverser = TraverseCodebase(self.code_base_model)
        self.search_result = traverser.get_top_nodes(query_keywords, 5)
        # Question Answer
        responder = QueryAnswer(self.search_result)
        response = responder.get_response(question)
        return response

class TestIntegration:
    def __init__(self):
        print("INTEGRATION TEST")
        test_code_base = "rust-calculator"
        test_ignore_file = "ignore.txt"
        self.integration = Integration(test_code_base, test_ignore_file)
    
    def test_run(self):
        print("modelling codebase...")
        self.integration.model_codebase()
        #Q1
        question = "Does this project have a multiplication capability?"
        print(f"Q: {question}")
        print("querying codebase...")
        response = self.integration.query(question)
        print(f"RESPONSE: \n{response}\n")
        #Q2
        question = "does it have a square operation functionality?"
        print(f"Q: {question}")
        print("querying codebase...")
        response = self.integration.query(question)
        print(f"RESPONSE: \n{response}\n")
        #Q3
        question = "how would we modify the code to add a square function?"
        print(f"Q: {question}")
        print("querying codebase...")
        response = self.integration.query(question)
        print(f"RESPONSE: \n{response}\n")
    
    def test_run_loop_prompt(self):
        print("modelling codebase...")
        self.integration.model_codebase()
        while True:
            question = input("QUESTION: ")
            print("querying codebase...")
            response = self.integration.query(question)
            print(f"RESPONSE: \n{response}\n")
        
        
if __name__ == "__main__":
    testIntegration = TestIntegration()
    testIntegration.test_run()
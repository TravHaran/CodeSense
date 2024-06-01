import sys

sys.path.insert(0, "..")
from src.codebase_extract.codebase_extract import CodebaseExtract
from src.codebase_extract.github_codebase_extract import CodeBaseExtractGithub
from src.populate_annotations.populate_annotations import PopulateAnnotations
from src.populate_annotations.batch_populate_annotations import BatchPopulateAnnotations
from src.populate_keywords.populate_keywords import PopulateKeywords
from src.keyword_extract.keyword_extract import KeywordExtract
from src.tree_traverse.tree_traverse import TraverseCodebase
from src.question_answering.question_answer import QueryAnswer
from src.question_answering.search import Search
from src.utilities.utility import obj_to_json, json_to_obj

class App:
    def model_code_base(self, code_base_path: str, ignore_paths) -> dict:
        # Extract Codebase
        if code_base_path.startswith("https://github.com"):
            codebase_extractor = CodeBaseExtractGithub(code_base_path)
        else: # a local directory path was passed
            codebase_extractor = CodebaseExtract(code_base_path)
        code_base_model = codebase_extractor.get_model()
        # Populate Annotations
        # populate_annotations = PopulateAnnotations(code_base_model, ignore_paths)
        # code_base_model = populate_annotations.populate_model()
        populate_annotations = BatchPopulateAnnotations(code_base_model, ignore_paths)
        code_base_model = populate_annotations.batch_annotate()
        # Populate Keywords
        populate_keywords = PopulateKeywords(code_base_model)
        code_base_model = populate_keywords.populate_model()
        return code_base_model
    
    def search_code_base(self, code_base_model: dict, question: str) -> dict:
        # Extract Keywords
        # print("EXTRACTING KEYWORDS")
        extract_keywords = KeywordExtract()
        query_keywords = extract_keywords.extract(question)
        # print(f"EXTRACTED KEYWORDS: {query_keywords}")
        # Traverse Tree
        # print("TRAVERSING TREE")
        traverser = TraverseCodebase(code_base_model)
        search_result = traverser.get_top_nodes(query_keywords, None)
        search_result['question'] = question
        # print(f"TREE TRAVERSAL: {search_result}")
        # Search Results
        # print("SEARCHING")
        responder = Search(search_result)
        results = responder.run()
        return results
    
    def query_code_base(self, code_base_model: dict, question: str, search_result_limit: int) -> dict:
        # Extract Keywords
        print("EXTRACTING KEYWORDS")
        extract_keywords = KeywordExtract()
        query_keywords = extract_keywords.extract(question)
        print(f"EXTRACTED KEYWORDS: {query_keywords}")
        # Traverse Tree
        print("TRAVERSING TREE")
        traverser = TraverseCodebase(code_base_model)
        search_result = traverser.get_top_nodes(query_keywords, search_result_limit)
        search_result['question'] = question
        print(f"TREE TRAVERSAL: {search_result}")
        # Question Answer
        print("ANSWERING QUESTION")
        responder = QueryAnswer(search_result)
        response = responder.get_response(question)
        search_result['answer'] = response
        print(f"SEARCH RESULT WITH ANSWER: {search_result}")
        return search_result

class TestApp:
    def __init__(self):
        self.test_github_repo = "https://github.com/TravHaran/rust-calculator"
        self.test_ignore = []
        self.app = App()
        
    def test_search(self):
        print("TESTING SEARCH")
        model = json_to_obj("./out/TravHaran_rust-calculator.json")
        question = "Does this project have a multiplication capability?"
        print(f"Q: {question}")
        response = self.app.search_code_base(model, question)
        obj_to_json("./out", "test_search", response)
        print(response)
    
    def test_run(self):
        print(f"modelling codebase from repo: {self.test_github_repo}")
        model = self.app.model_code_base(self.test_github_repo, self.test_ignore)
        # Save final model
        obj_to_json("./out", "codebase", model)
        #Q1
        question = "Does this project have a multiplication capability?"
        print(f"Q: {question}")
        print("querying codebase...")
        response = self.app.query_code_base(model, question, 3)
        ans = response["answer"]
        print(f"RESPONSE: \n{ans}\n")
        #Q2
        question = "does it have a square operation functionality?"
        print(f"Q: {question}")
        print("querying codebase...")
        response = self.app.query_code_base(model, question, 3)
        ans = response["answer"]
        print(f"RESPONSE: \n{ans}\n")
        #Q3
        question = "how would we modify the code to add a square function?"
        print(f"Q: {question}")
        print("querying codebase...")
        response = self.app.query_code_base(model, question, 3)
        ans = response["answer"]
        print(f"RESPONSE: \n{ans}\n")
        
if __name__ == "__main__":
    testApp = TestApp()
    # testApp.test_run()   
    testApp.test_search()  
        

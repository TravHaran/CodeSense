import threading
from queue import Queue
import sys

sys.path.insert(0, "..")
from app import App
from utilities.utility import obj_to_json, json_to_obj, get_matched_keywords, convert_words_to_lowercase
from tree_traverse.tree_traverse import TraverseCodebase
from keyword_extract.keyword_extract import KeywordExtract
from question_answering.question_answer import QueryAnswer

'''
define a class that can query multiple codebases and return an answer
- use multithreading
- input:
    - batch modeled codebases object
    - question as a string
- output:
    - answer a string
'''

class BatchQuery:
    def __init__(self, batch_models: dict, question: str, search_result_limit: int):
        self.models = batch_models["results"]
        self.num_threads = len(self.models)
        self.q = Queue(maxsize=0)
        self.query = question
        self.query_keywords = KeywordExtract().extract(question)
        self.limit = search_result_limit
        self.top_nodes = []
        self.answer = ""
        
    def query_codebase(self, q, output_list):
        while True:
            model = q.get()
            search_result = TraverseCodebase(model).get_top_nodes(self.query_keywords, self.limit)
            nodes = search_result["results"]
            for node in nodes:
                score = node["score"]
                output_list.append((score, node))
            q.task_done()
    
    def run(self) -> dict:
        for i in range(self.num_threads):
            worker = threading.Thread(
                target=self.query_codebase, daemon=True, args=(self.q, self.top_nodes))
            worker.start()
        
        for model in self.models:
            self.q.put(model)
        self.q.join()
        
        # after traversal sort top_nodes list by score in descending order
        self.top_nodes.sort(key=lambda x: x[0], reverse=True)
        # build search_result output
        search_result = {"question": self.query, "answer": "", "input_keywords": self.query_keywords, "results": []}
        lowered_input_keywords = convert_words_to_lowercase(self.query_keywords)
        for entry in self.top_nodes:
            score = entry[0]
            node = entry[1]["node"]
            # print(node)
            # add matched keywords attribute
            matched_keywords = get_matched_keywords(
                node["keywords"], lowered_input_keywords)
            entry = {'score': score, 'matched_keywords': matched_keywords, 'node': node}
            search_result["results"].append(entry)
        search_result["results"] = search_result["results"][:self.limit]
        self.answer = QueryAnswer(search_result).get_response(self.query)
        search_result["answer"] = self.answer
        return search_result

class TestBatchQuery:
    def __init__(self):
        self.test_batch_codebase_models = json_to_obj("batch_model_codebase.json")     
    
    def test_batch(self):
        #Q1
        question = "is there a multiplication capability in these projects?"
        print("querying codebase...")
        batchQuery = BatchQuery(self.test_batch_codebase_models, question, 5)
        response = batchQuery.run()
        ans = response["answer"]
        print(f"RESPONSE: \n{ans}\n")
        obj_to_json("../out", "batch_query_codebase", response)

if __name__ == "__main__":
    testBatchQuery = TestBatchQuery()
    testBatchQuery.test_batch()
    
        
            
        
        
import sys

sys.path.insert(0, "..")

from src.question_answering.question_answer import QueryAnswer
from src.question_answering.search import Search
from src.keyword_extract.keyword_extract import KeywordExtract
from src.tree_traverse.tree_traverse import TraverseCodebase
from src.utilities.utility import obj_to_json, json_to_obj, get_matched_keywords, convert_words_to_lowercase
from src.app import App
import threading
from queue import Queue

'''
define a class that can search multiple codebases and return an answer
- use multithreading
- input:
    - batch modeled codebases object
    - question as a string
- output:
    - results object
'''

class BatchSearch:
    def __init__(self, batch_models: dict, question: str):
        self.threads = []
        self.models = batch_models["results"]
        self.max_threads = 5
        self.q = Queue(maxsize=0)
        self.query = question
        self.query_keywords = KeywordExtract().extract(question)
        self.top_nodes = []
    
    def query_codebase(self, model):
        search_result = TraverseCodebase(model).get_top_nodes(
            self.query_keywords, None)
        nodes = search_result["results"]
        for node in nodes:
            score = node["score"]
            self.q.put((score, node))
    
    def run(self) -> dict:
        for model in self.models:
            self.threads.append(threading.Thread(
                target=self.query_codebase, args=(model, )))
            
        if len(self.threads) > self.max_threads:
            self._run_multi_pool()
        else:
            self._run_single_pool()
        return self._build_result()
    
    def _run_single_pool(self):
        for x in self.threads:
            x.start()
        for x in self.threads:
            x.join()

    def _run_multi_pool(self):
        for i in range(0, len(self.threads), self.max_threads):
            pool = self.threads[i: i+self.max_threads]
            for j in pool:
                j.start()
            for j in pool:
                j.join()
    
    def _build_result(self):
        while not self.q.empty():
            entry = self.q.get()
            self.top_nodes.append(entry)

        # after traversal sort top_nodes list by score in descending order
        self.top_nodes.sort(key=lambda x: x[0], reverse=True)
        # build search_result output
        search_result = {"question": self.query, "answer": "",
                         "input_keywords": self.query_keywords, "results": []}
        lowered_input_keywords = convert_words_to_lowercase(
            self.query_keywords)
        for entry in self.top_nodes:
            score = entry[0]
            node = entry[1]["node"]
            # print(node)
            # add matched keywords attribute
            matched_keywords = get_matched_keywords(
                node["keywords"], lowered_input_keywords)
            entry = {'score': score,
                     'matched_keywords': matched_keywords, 'node': node}
            search_result["results"].append(entry)
        responder = Search(search_result)
        results = responder.run()
        return results

class TestBatchSearch:
    def __init__(self):
        self.test_batch_codebase_models = json_to_obj(
            "batch_model_codebase.json")
    
    def test_batch(self):
        # Q1
        question = "is there a multiplication capability in these projects?"
        print("searching codebase...")
        batchSearch = BatchSearch(self.test_batch_codebase_models, question)
        response = batchSearch.run()
        print(f"RESPONSE: \n{response}\n")
        obj_to_json("../out", "batch_search_codebase", response)

if __name__ == "__main__":
    testBatchSearch = TestBatchSearch()
    testBatchSearch.test_batch()

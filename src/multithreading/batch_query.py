import sys

sys.path.insert(0, "..")

from src.question_answering.question_answer import QueryAnswer
from src.keyword_extract.keyword_extract import KeywordExtract
from src.tree_traverse.tree_traverse import TraverseCodebase
from src.utilities.utility import obj_to_json, json_to_obj, get_matched_keywords, convert_words_to_lowercase
from src.app import App
import threading
from queue import Queue


'''
define a class that can query multiple codebases and return an answer
- use multithreading
- input:
    - batch modeled codebases object
    - question as a string
- output:
    - results object
'''


class BatchQuery:
    def __init__(self, batch_models: dict, question: str, search_result_limit: int):
        self.threads = []
        self.models = batch_models["results"]
        self.max_threads = 5
        self.q = Queue(maxsize=0)
        self.query = question
        self.query_keywords = KeywordExtract().extract(question)
        self.limit = search_result_limit
        self.top_nodes = []

    def query_codebase(self, model):
        search_result = TraverseCodebase(model).get_top_nodes(
            self.query_keywords, self.limit)
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
        search_result["results"] = search_result["results"][:self.limit]
        answer = QueryAnswer(search_result).get_response(self.query)
        search_result["answer"] = answer
        return search_result


class TestBatchQuery:
    def __init__(self):
        self.test_batch_codebase_models = json_to_obj(
            "batch_model_codebase.json")

    def test_batch(self):
        # Q1
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

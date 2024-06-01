'''
Create a class that can extract the call graph for a code file
and extract the snippets of code for each node in the graph

save as a json
'''


import ast
import json

class CallExtractor(ast.NodeVisitor):
    def __init__(self):
        self.call_hierarchy = []

    def visit_Call(self, node):
        call = {
            "class": None,
            "function_name": None,
            "calls": []
        }
        if hasattr(node.func, 'value') and isinstance(node.func.value, ast.Name):
            call["class"] = node.func.value.id
        if isinstance(node.func, ast.Attribute):
            call["function_name"] = node.func.attr
        elif isinstance(node.func, ast.Name):
            call["function_name"] = node.func.id
        for arg in node.args:
            if isinstance(arg, ast.Call):
                call["calls"].append(self.visit_Call(arg))
        self.call_hierarchy.append(call)
        self.generic_visit(node)

def parse_code_and_write_json(code_string, output_filename):
    tree = ast.parse(code_string)
    extractor = CallExtractor()
    extractor.visit(tree)
    
    def build_nested_call_hierarchy(calls):
        call_hierarchy = []
        for call in calls:
            if call:
                call_obj = {
                    "class": call["class"],
                    "function_name": call["function_name"],
                    "calls": build_nested_call_hierarchy(call["calls"])
                }
                call_hierarchy.append(call_obj)
        return call_hierarchy
    
    nested_call_hierarchy = build_nested_call_hierarchy(extractor.call_hierarchy)
    
    with open(output_filename, 'w') as f:
        json.dump(nested_call_hierarchy, f, indent=4)

if __name__ == "__main__":
    input_code = """
import sys

sys.path.insert(0, "..")

from question_answering.question_answer import QueryAnswer
from keyword_extract.keyword_extract import KeywordExtract
from tree_traverse.tree_traverse import TraverseCodebase
from utilities.utility import obj_to_json, json_to_obj, get_matched_keywords, convert_words_to_lowercase
from app import App
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
        print(f"RESPONSE: {ans}")
        obj_to_json("../out", "batch_query_codebase", response)


if __name__ == "__main__":
    testBatchQuery = TestBatchQuery()
    testBatchQuery.test_batch()

"""
    output_filename = "call_hierarchy.json"
    parse_code_and_write_json(input_code, output_filename)

    print("Call hierarchy saved to 'call_hierarchy.json'")
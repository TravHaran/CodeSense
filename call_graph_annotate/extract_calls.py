'''
Create a class that can extract the call graph for a code file
and extract the snippets of code for each node in the graph

save as a json
'''


import ast
import json

import ast
import json

class CallHierarchyExtractor(ast.NodeVisitor):
    def __init__(self, source_code):
        self.call_hierarchy = {}
        self.current_function = None
        self.source_code = source_code
        self.current_class = None

    def visit_FunctionDef(self, node):
        function_name = node.name
        if function_name not in self.call_hierarchy:
            self.call_hierarchy[function_name] = []
        self.current_function = function_name
        self.generic_visit(node)
        self.current_function = None

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            function_name = node.func.id
            if self.current_function:
                call_snippet = ast.get_source_segment(self.source_code, node)
                self.call_hierarchy[self.current_function].append({
                    "function_name": function_name,
                    "code_snippet": call_snippet
                })
        self.generic_visit(node)

def extract_call_hierarchy(source_code):
    tree = ast.parse(source_code)
    extractor = CallHierarchyExtractor(source_code)
    extractor.visit(tree)
    return extractor.call_hierarchy

def save_as_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Example usage
source_code = """
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


call_hierarchy = extract_call_hierarchy(source_code)
save_as_json(call_hierarchy, 'call_hierarchy.json')

print("Call hierarchy saved to 'call_hierarchy.json'")

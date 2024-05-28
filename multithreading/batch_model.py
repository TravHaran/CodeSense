import sys

sys.path.insert(0, "..")

from app import App
from utilities.utility import obj_to_json
import threading
from queue import Queue

'''
define a class that can accept a list of codebases and model them
- use multithreading
- input: list of strings
- output: list of modeled codebase objects
'''


class BatchModel:
    def __init__(self, codebases: list[(str, dict)]):
        self.threads = []
        self.max_threads = 5
        self.q = Queue(maxsize=0)
        self.input_codebases = codebases
        
        self.result = []

    def model_codebase(self, codebase, ignores):
        model = App().model_code_base(codebase, ignores)
        self.q.put(model)

    def run(self) -> dict:
        for entry in self.input_codebases:
            codebase = entry[0]
            ignores = entry[1]
            self.threads.append(threading.Thread(
                target=self.model_codebase, args=(codebase, ignores)))
            
        if len(self.input_codebases) > self.max_threads:
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
            model = self.q.get()
            self.result.append(model)
        output = {"results": self.result}
        return output


class TestBatchModel:
    def __init__(self):
        self.test_codebases_list = [
            ("https://github.com/TravHaran/rust-calculator", {"ignore": []}),
            ("https://github.com/sachinl0har/Basic-Calc",
             {"ignore": ["README.md"]})
        ]

    def test_batch(self):
        batchModel = BatchModel(self.test_codebases_list)
        output = batchModel.run()
        obj_to_json("../out", "batch_model_codebase", output)


if __name__ == "__main__":
    testBatchModel = TestBatchModel()
    testBatchModel.test_batch()

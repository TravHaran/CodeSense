import threading
from queue import Queue
import sys

sys.path.insert(0, "..")
from utilities.utility import obj_to_json
from app import App
'''
define a class that can accept a list of codebases and model them
- use multithreading
- input: list of strings
- output: list of modeled codebase objects
'''


class BatchModel:
    def __init__(self, codebases: list[(str, dict)]):
        # TODO implement a thread pool such that if the number of input codebases is below the maxthreads limit 
        # it runs all operations within the pool, but if not if allocates enough pools to complete the batch request
        self.num_threads = len(codebases) # change this to something like 5.
        self.q = Queue(maxsize=0)
        self.input_codebases = codebases
        self.result = []

    def model_codebase(self, q, output_list):
        while True:
            entry = q.get()
            codebase = entry[0]
            ignores = entry[1]
            model = App().model_code_base(codebase, ignores)
            output_list.append(model)
            q.task_done()

    def run(self) -> dict:
        for i in range(self.num_threads):
            worker = threading.Thread(
                target=self.model_codebase, daemon=True, args=(self.q, self.result))
            worker.start()

        for entry in self.input_codebases:
            self.q.put(entry)
        self.q.join()
        return self.result


class TestBatchModel:
    def __init__(self):
        self.test_codebases_list = [
            ("https://github.com/TravHaran/rust-calculator", {"ignore": []}),
            ("https://github.com/sachinl0har/Basic-Calc",
             {"ignore": ["README.md"]})
        ]

    def test_batch(self):
        batchModel = BatchModel(self.test_codebases_list)
        output = {"results": []}
        output["results"] = batchModel.run()
        obj_to_json("../out", "batch_model_codebase", output)


if __name__ == "__main__":
    testBatchModel = TestBatchModel()
    testBatchModel.test_batch()

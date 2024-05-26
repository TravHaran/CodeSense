import json

'''
Create a class to aggregate the annotations of some target nodes
- input:
    - search_result json file containing most relevant nodes with annotations 
- output:
    - an aggregate of all the relevant annotations in string format
    - optionally save output as txt file
'''

class AnnotationAggregate:
    def __init__(self, search_result_file_path):
        self.file_path = search_result_file_path
        self.result_model = self.load_model()
        self.annotations = []
    
    def aggregate_annotations(self):
        for entry in self.result_model["results"]:
            node = entry["node"]
            self.annotations.append((node["name"], node["annotation"]))
        return self.format_output()
    
    def format_output(self):
        output = "Relevant Files: \n\n"
        count = 0
        for entry in self.annotations:
            count += 1
            name = entry[0]
            annotation = entry[1]
            output += str(f"FILENAME: {name}\nDESCRIPTION: \"{annotation}\"\n\n")
        return output
          
    def load_model(self):
        d = {}
        with open(self.file_path) as json_data:
            d = json.load(json_data)
        return d

class TestAnnotationAggregate:
    def test_aggreagate_top_1_results(self):
        test_json_file = "/Users/trav/Documents/projects/codesense/annotation_aggregate/top_1.json"
        aggregator = AnnotationAggregate(test_json_file)
        print("\nTesting Aggregation of top 1 results:")
        result = aggregator.aggregate_annotations()
        print(result)
    def test_aggreagate_top_3_results(self):
        test_json_file = "/Users/trav/Documents/projects/codesense/annotation_aggregate/top_3.json"
        aggregator = AnnotationAggregate(test_json_file)
        print("\nTesting Aggregation of top 3 results:")
        print(aggregator.aggregate_annotations())
        
    def test_aggreagate_top_10_results(self):
        test_json_file = "/Users/trav/Documents/projects/codesense/annotation_aggregate/top_10.json"
        aggregator = AnnotationAggregate(test_json_file)
        print("\nTesting Aggregation of top 10 results:")
        print(aggregator.aggregate_annotations())

if __name__ == "__main__":
    testAnnotationAggregate = TestAnnotationAggregate()
    testAnnotationAggregate.test_aggreagate_top_1_results()
    testAnnotationAggregate.test_aggreagate_top_3_results()
    testAnnotationAggregate.test_aggreagate_top_10_results()
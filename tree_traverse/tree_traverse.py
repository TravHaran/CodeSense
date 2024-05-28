import sys

sys.path.insert(0, "..")
from utilities.utility import obj_to_json, json_to_obj, compute_score, convert_words_to_lowercase, get_matched_keywords

'''
Create a class to find the most relevant node in the codebase model given some keywords
- input:
    - list of keywords
    - codebase model object
- output:
    - object of top nodes containing: file_name, annotation, content, and matching_keywords
'''


class TraverseCodebase:
    def __init__(self, model_obj):
        self.model = model_obj
        self.top_nodes_with_score = []
        self.result_file_name = "result"

    def get_top_nodes(self, input_keywords, n):
        # we need to reset the top_nodes list to empty so that multiple calls of this method don't append to it
        self.top_nodes_with_score = []
        # lower input keywords to compute score properly
        input_keywords_lowered = convert_words_to_lowercase(
            input_keywords)
        # recursively populate top_nodes list
        self._get_top_nodes(self.model, input_keywords_lowered)
        # after traversal sort top_nodes list by score in descending order
        self.top_nodes_with_score.sort(key=lambda x: x[0], reverse=True)  
        # return result
        return self.build_result(n, input_keywords_lowered)

    def _get_top_nodes(self, model, input_keywords):
        if model["type"] == "file":
            # get matching keyword score
            score = compute_score(model["keywords"], input_keywords)
            self.top_nodes_with_score.append((score, model))
            return model
        else:
            for child in model["children"]:
                self._get_top_nodes(child, input_keywords)

    def build_result(self, n, input_keywords):
        result = {"input_keywords": input_keywords, "results": []}
        for entry in self.top_nodes_with_score:
            score = entry[0]
            node = entry[1]
            # add matched keywords attribute
            matched_keywords = get_matched_keywords(
                node["keywords"], input_keywords)
            entry = {'score': score, 'matched_keywords': matched_keywords, 'node': node}
            result["results"].append(entry)
        result["results"] = result["results"][:n]
        return result

    


class TestTraverseCodebase:
    def __init__(self):
        self.test_model = json_to_obj("test_codebase.json")
        self.traverser = TraverseCodebase(self.test_model)

    def test_save_top_1_nodes(self):
        print(f"Testing Traverse Codebase to save top 1 nodes")
        input_keywords = ["Python", "function", "TestKeywordExtract",
                          "NLTK", "Word2Vec", "extract_keywords"]
        updated_model = self.traverser.get_top_nodes(input_keywords, 1)
        obj_to_json("./", "top_1", updated_model)
        assert type(updated_model) == dict

    def test_save_top_3_nodes(self):
        print(f"Testing Traverse Codebase to save top 3 nodes")
        input_keywords = ["Python", "function", "TestKeywordExtract",
                          "NLTK", "Word2Vec", "extract_keywords"]
        updated_model = self.traverser.get_top_nodes(input_keywords, 3)
        obj_to_json("./", "top_3", updated_model)
        assert type(updated_model) == dict

    def test_save_top_5_nodes(self):
        print(f"Testing Traverse Codebase to save top 5 nodes")
        input_keywords = ["Python", "function", "TestKeywordExtract",
                          "NLTK", "Word2Vec", "extract_keywords"]
        updated_model = self.traverser.get_top_nodes(input_keywords, 5)
        obj_to_json("./", "top_5", updated_model)
        assert type(updated_model) == dict


if __name__ == "__main__":
    testTraverseCodebase = TestTraverseCodebase()
    testTraverseCodebase.test_save_top_1_nodes()
    testTraverseCodebase.test_save_top_3_nodes()
    testTraverseCodebase.test_save_top_5_nodes()


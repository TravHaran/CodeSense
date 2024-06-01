import sys 
import re

sys.path.insert(0, "..")
from src.utilities.utility import json_to_obj, obj_to_json
from src.keyword_extract.keyword_extract import KeywordExtract

'''
Create a class that returns the search results for a query
- input: traversal result object
- output: modified traversal result object
    - given the annotation of a relevant file
        - highlight the matched keyword in markdown
    - save this as an attribute called highlights
'''

class Search:
    def __init__(self, traverse_obj):
        self.traversal = traverse_obj
        self.highlights = []
    
    def run(self):
        for entry in self.traversal['results']:
            keywords = entry['matched_keywords']
            node = entry['node']
            annotation = node["annotation"]
            highlights = self._highlight(annotation, keywords)
            # Create new highlights attribute
            entry['highlights'] = highlights
        return self.traversal

    def _highlight(self, text, words_to_highlight) -> str:
        # perform case-insensitive search and replacement
        words_to_highlight.sort(key=len, reverse=True)
        for word in words_to_highlight:
            # Use a placeholder to avoid nested replacements
            placeholder = f"{{{{HIGHLIGHT_{word}}}}}"
            text = text.replace(word, placeholder)
        # Replace placeholders with bold Markdown syntax
        for word in words_to_highlight:
            placeholder = f"{{{{HIGHLIGHT_{word}}}}}"
            text = text.replace(placeholder, f"**{word}**")
        return text

class TestSearch:
    def __init__(self):
        self.test_traverse_obj = json_to_obj("test_traverse.json")
    
    def test_search_insert_highlights(self):
        responder = Search(self.test_traverse_obj)
        result = responder.run()
        print(result)
        obj_to_json("./", "test_search_response", result)
        assert type(result) == dict

if __name__ == "__main__":
    testSearch = TestSearch()
    testSearch.test_search_insert_highlights()
        
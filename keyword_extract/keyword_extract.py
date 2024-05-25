import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


'''
Create a class to extract keywords from text
- input:
    - sample text as a string
-output: 
    - list of keywords
'''


class KeywordExtract:
    def __init__(self):
        self.keywords = []
        # common english stopwords
        self.stop_words = set(stopwords.words("english"))

    def extract(self, text):
        tokens = word_tokenize(text)  # tokenize text
        filtered_tokens = [word for word in tokens if word.lower(
        ) not in self.stop_words]  # filter out stopwords
        # identify keywords with part of speech tagging
        pos_tags = nltk.pos_tag(filtered_tokens)
        # keep only nouns, verbs
        for word, pos in pos_tags:
            if pos.startswith("NN") or pos.startswith("VB"):
                self.keywords.append(word)
        self.keywords = list(set(self.keywords))  # remove duplicates
        return self.keywords


class TestKeywordExtract:
    def __init__(self):
        self.extractor = KeywordExtract()
        print("Testing Keyword Extractor...\n")

    def test_extract_keywords_from_query(self):
        print("Testing keywword extraction of user query...\n")
        text = "I want to modify the maxProfit function to have an initial maxP value of 10"
        output = self.extractor.extract(text)
        print(f"Keywords from query: {output}\n")
        assert type(output) == list

    def test_extract_keywords_from_annotation(self):
        print("Testing keywword extraction of code annotation...\n")
        text = """
            The maxProfit function is part of a C++ class Solution. It calculates the maximum profit that can be made from a list of stock prices (prices). The function follows these steps:

            Initialize Profit: It initializes maxP, the maximum profit, to 0.
            Iterate Through Prices: It loops through the list of prices from the second element (index 1) to the end.
            Calculate Profit: If the current price is higher than the previous price, it calculates the profit by subtracting the previous price from the current price and adds it to maxP.
            Return Profit: The function returns the accumulated maxP as the maximum profit.
            Overall, this function implements a simple algorithm for finding the total profit from multiple price increases in a stock price list, where each increase represents a buy-and-sell opportunity.
            """
        output = self.extractor.extract(text)
        print(f"Keywords from annotation: {output}\n")
        assert type(output) == list


if __name__ == "__main__":
    testKeywordExtract = TestKeywordExtract()
    testKeywordExtract.test_extract_keywords_from_query()
    testKeywordExtract.test_extract_keywords_from_annotation()

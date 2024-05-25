import nltk
import gensim.downloader
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import warnings

input_text1 = """
I want to modify the maxProfit function to have an initial maxP value of 10
"""

input_text2 = """
The maxProfit function is part of a C++ class Solution. It calculates the maximum profit that can be made from a list of stock prices (prices). The function follows these steps:

Initialize Profit: It initializes maxP, the maximum profit, to 0.
Iterate Through Prices: It loops through the list of prices from the second element (index 1) to the end.
Calculate Profit: If the current price is higher than the previous price, it calculates the profit by subtracting the previous price from the current price and adds it to maxP.
Return Profit: The function returns the accumulated maxP as the maximum profit.
Overall, this function implements a simple algorithm for finding the total profit from multiple price increases in a stock price list, where each increase represents a buy-and-sell opportunity.
"""

#######################extract keywords#######################

#download necessary resources
# nltk.download('averaged_perceptron_tagger')
# nltk.download("punkt")
# nltk.download("stopwords")

def extract_keywords(text):
    #tokenize the text into words
    tokens = word_tokenize(text)
    #define a set of common English stopwords
    stop_words = set(stopwords.words("english"))
    #filter out stopwords and keep significant words(i.e. nouns, verbs)
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    keywords = []
    #identify keywords using part-of-speech tagging
    pos_tags = nltk.pos_tag(filtered_tokens)
    #keep only nouns, proper nouns, and verbs
    for word, pos in pos_tags:
        if pos.startswith("NN") or pos.startswith("VB"):
            keywords.append(word)
    unique_keywords = list(set(keywords))
    return unique_keywords

# print(extract_keywords(input_text1))

#######################compute the similarity between keywords#######################

warnings.filterwarnings(action='ignore')
#  Reads ‘context.txt’ file (for our application this will be the aggrgated summary report for a code file)
sample = open("/Users/trav/Documents/projects/codesense/keyword_extraction/context.txt")
s = sample.read()
# Replaces escape character with space
f = s.replace("\n", " ")
data = []
# iterate through each sentence in the file
for i in sent_tokenize(f):
    temp = []
    # tokenize the sentence into words
    for j in word_tokenize(i):
        temp.append(j.lower())
    data.append(temp)
model = gensim.models.Word2Vec(data, min_count=1,
                                vector_size=100, window=5, sg=1)

def compare_words(w1, w2):
    if w1 == w2:
        return 1
    if w1 in model.wv and w2 in model.wv:
        return model.wv.similarity(w1, w2)
    else:
        return 0

def compare_keywords(l1, l2):
    output = 0
    for word1 in l1:
        word1 = word1.lower()
        for word2 in l2:
            output += compare_words(word1, word2.lower())
    return output

list1 = extract_keywords(input_text1)
list2 = extract_keywords(input_text2)
print(compare_keywords(list1, list2))

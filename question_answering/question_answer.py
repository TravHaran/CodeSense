from openai import OpenAI
import os
from dotenv import load_dotenv
import sys

sys.path.insert(0, "..")
from annotation_aggregate.annotation_aggregate import AnnotationAggregate
from utilities.utility import json_to_obj

'''
Create a class that responds to a user query given context from the codebase
- input:
    - traversal result object
- output:
    - Response to user query as string
'''


class QueryAnswer:
    def __init__(self, traverse_obj):
        self.res = ""
        self.traversal = traverse_obj
        self.context = self.pre_process()
    
    def pre_process(self) -> str:
        context = ""
        if self.traversal['results'] != []:
            aggregator = AnnotationAggregate(self.traversal)
            context = aggregator.aggregate_annotations()
        return context    
        
    def get_response(self, query):
        response = ""
        if self.context == "":
            response = f"Your question did not match any files\n\nSuggestions:\n\n- Make sure all words are spelled correctly.\n- Try different keywords.\n- Try more general keywords"
        else:
            response = self._generate_response(query)
        return response
    
    ## Set the API Key
    def _generate_response(self, query):
        load_dotenv()
        API_KEY = os.getenv('OPENAI_SECRET_API_KEY')
        client = OpenAI(api_key=API_KEY)

        #GPT4o REPONSE REQUEST
        MODEL="gpt-4o"

        completion = client.chat.completions.create(
        model=MODEL,
        #Prompt modelling, grounding the model to provide a more concise and clear summary when given a piece of code
        messages=[
            {"role": "system", "content": '''
            You are a developer assistant designed to provide detailed answers and assistance based on contextual explanations of code in a codebase. Your input consists of explanations of code files and their respective file directories within the codebase. Users will provide queries related to the codebase, seeking clarification, assistance, or suggestions. Your task is to utilize the provided context to generate clear and structured responses to the user queries. Your responses should be informative, accurate, and tailored to the specific query. Additionally, you may suggest potential actions or direct the user to relevant code files within the codebase for further reference. Your responses should solely rely on the provided context, avoiding external knowledge or assumptions. Remember to maintain clarity and coherence in your responses, ensuring that users can easily understand and follow your guidance. Make sure to keep your responses as short as possible as well so that the developer can quickly view an answer their question.
            DO NOT HAVE THE QUERY IN YOUR REPONSE

            Example:

            Query: How does the event-handling function handle errors during Firestore database operations?

            Context:
            The code is written in JavaScript, specifically using the async/await syntax to handle asynchronous operations with Firestore, a cloud database from Firebase. It defines an event-handling function `handleCreateEvent` meant to create and save event data into the Firestore database. When a form submission event triggers the function, it first prevents the default behavior with `e.preventDefault()`. The function checks if `isDateRange` is false and, based on this, either adds or updates single or range-dated event documents in the Firestore under the 'events' collection. It also conditionally updates the 'announcements' collection based on the existence of date ranges. After database operations, it resets multiple state variables (title, description, dateTime, etc.) and fetches user data. The function ensures newly created or modified data incorporates the current date and time and user metadata. The expected result includes adding appropriate entries in the Firestore under both 'events' and 'announcements' collections and resetting the form's state. 
            File Directory: NewsFlash/pages/events.js
            

            Response:
            The event-handling function `handleCreateEvent` in the file events.js employs error handling mechanisms to manage errors during Firestore database operations. Within the async function, try-catch blocks are utilized to capture and handle any potential errors that may occur during asynchronous database transactions. Specifically, when performing Firestore operations such as adding or updating event documents, the try block encapsulates these operations, allowing for graceful error handling. In the event of an error, the catch block is triggered, enabling the function to handle the error appropriately, which may include logging the error, displaying a user-friendly message, or initiating corrective actions. Additionally, the function may utilize Firebase's error handling features, such as error codes or error objects, to provide more detailed information about the nature of the error and facilitate troubleshooting. Overall, the event-handling function is designed to handle errors robustly, ensuring the reliability and stability of database operations.
            '''},

            {"role": "user", "content": f'''With that said. The query and context is given below:
            QUERY: {query}
            
            CODEBASE CONTEXT: {self.context}
            '''}
        ]
        )
        return completion.choices[0].message.content

### TESTING 
class TestQueryAnswering:
    def __init__(self):
        self.test_traverse = json_to_obj("top_5.json")
        self.test_traverse_empty = json_to_obj("top_0.json")
        
        print("Testing Query Response... \n")
    
    
    def test_query_with_no_matching_files(self):
        responder = QueryAnswer(self.test_traverse_empty)
        query="daslfjadslkf"
        expected_response = f"Your question did not match any files\n\nSuggestions:\n\n- Make sure all words are spelled correctly.\n- Try different keywords.\n- Try more general keywords"
        output = responder.get_response(query)
        print(output)
        assert output == expected_response      
    
    def test_keyword_extract_explanation(self):
        responder = QueryAnswer(self.test_traverse)
        query="How does keyword extraction work in this project?"
        output = responder.get_response(query)
        print(output)
        assert type(output) == str
    

if __name__ == "__main__":
    TestQueryAnswering = TestQueryAnswering()
    TestQueryAnswering.test_query_with_no_matching_files()
    TestQueryAnswering.test_keyword_extract_explanation()
from openai import OpenAI
import os
from dotenv import load_dotenv

'''
Create a response to a user query given context from the codebase
- input:
    - User query
    - Code Context (Function, Class, etc.)
- output:
    - Response to user query
'''


class QueryAnswer:
    def __init__(self):
        self.res = ""
    

    ## Set the API Key
    def get_response_from_gpt(self, query, context):
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
            You are a developer assistant designed to provide detailed answers and assistance based on contextual explanations of code in a codebase. Your input consists of explanations of code files and their respective file directories within the codebase. Users will provide queries related to the codebase, seeking clarification, assistance, or suggestions. Your task is to utilize the provided context to generate clear and structured responses to the user queries. Your responses should be informative, accurate, and tailored to the specific query. Additionally, you may suggest potential actions or direct the user to relevant code files within the codebase for further reference. Your responses should solely rely on the provided context, avoiding external knowledge or assumptions. Remember to maintain clarity and coherence in your responses, ensuring that users can easily understand and follow your guidance.

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
            
            CODEBASE CONTEXT: {context}
            '''}
        ]
        )
        return completion.choices[0].message.content

### TESTING 
class TestQueryAnswering:
     def __init__(self):
        self.responder = QueryAnswer()
        print("Testing Query Response... \n")

     def query_response(self):
        context = '''
        File 1: authentication.js
        The code is written in TypeScript, utilizing the Firebase Authentication module to handle user authentication within the application. This file defines various functions for user authentication, including `registerUser`, `loginUser`, and `logoutUser`. The `registerUser` function accepts user credentials (email and password) as parameters and utilizes Firebase's authentication API to create a new user account. Upon successful registration, the function returns a user object containing user information such as UID and email. The `loginUser` function allows existing users to log in by providing their credentials, which are authenticated against Firebase's user database. If the authentication is successful, the function returns the user object corresponding to the authenticated user. Additionally, the file includes error handling mechanisms to manage authentication errors, such as incorrect credentials or network issues. File Directory: /src/utils/authentication.ts

        File 2: dashboard.js
        This JavaScript file serves as the main dashboard component of the application. It is responsible for fetching and displaying user-specific data retrieved from Firebase Firestore and Realtime Database. The `fetchUserData` function asynchronously retrieves user data from Firestore, including user profile information, preferences, and recent activity. The retrieved data is then utilized to dynamically populate various components of the dashboard interface. Additionally, the file contains event listeners to handle user interactions, such as clicking on navigation links or updating preferences. File Directory: /src/components/dashboard/Dashboard.js
        File 3: utils.js
        The `utils.js` file contains utility functions used across multiple components of the application. These functions include `formatDate`, `capitalizeString`, and `generateUniqueId`. The `formatDate` function takes a date object as input and formats it into a human-readable date string. The `capitalizeString` function capitalizes the first letter of a given string. Lastly, the `generateUniqueId` function generates a unique identifier using a combination of timestamp and random characters. These utility functions enhance code readability, maintainability, and reusability throughout the application. File Directory: /src/utils/utils.js
        '''
        query="How does the authentication system handle password reset requests?"
        output = self.responder.get_response_from_gpt(query, context)
        print(f"CONTEXT: \n{context} \n\n")
        print(f"QUERY: \n{query} \n\n")
        print(f"RESPONSE: \n{output} \n\n")

        assert type(output) == str

if __name__ == "__main__":
    TestQueryAnswering = TestQueryAnswering()
    TestQueryAnswering.query_response()
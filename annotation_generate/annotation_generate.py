from openai import OpenAI
import os
from dotenv import load_dotenv
from markdown import Markdown
from io import StringIO

'''
Create a class to annotate a piece of given code
- input:
    - Code (Function, Class, etc.)
- output:
    - Summary of code in text
'''

class AnnotationGeneration:
    def __init__(self):
        self.res = ""
    
    def run(self, snippet):
        annotation = self.snippet_summary(snippet)
        return self._markdown_to_plaintxt(annotation)
    
    def _snippet_summary(self, snippet):
        ## Set the API Key
        load_dotenv()
        API_KEY = os.getenv('OPENAI_SECRET_API_KEY')
        client = OpenAI(api_key=API_KEY)

        #GPT4o REPONSE REQUEST
        MODEL="gpt-4o"

        completion = client.chat.completions.create(
            model=MODEL,
            #Prompt modelling, grounding the model to provide a more concise and clear summary when given a piece of code
            messages=[
                {"role": "system", "content": '''You are an AI designed to explain code clearly and concisely. When given a piece of code, your task is to provide a quick summary without giving a detailed breakdown. Your summary should include the programming language, the purpose of the code, a brief explanation of its key components functionality and logic, and the expected output. Respond in a single blurb of text.

            Here is the piece of code for you to explain:

            python
            Copy code
            def is_prime(n):
                if n <= 1:
                    return False
                for i in range(2, int(n**0.5) + 1):
                    if n % i == 0:
                        return False
                return True

            number = 7
            result = is_prime(number)
            print(f"Is {number} a prime number? {result}")
            Expected Explanation:

            The code is written in Python and checks if a given number is a prime number. The function is_prime(n) returns True if n is prime by testing divisibility from 2 to the square root of n, otherwise it returns False. The variable number is set to 7, and the function is called to check if 7 is prime, with the result printed. The output will be: "Is 7 a prime number? True".'''},
                
                {"role": "user", "content": f'''With that said. Explain the given code:
                    {snippet}
                '''}
            ]
        )
        
        return completion.choices[0].message.content
    
    def _unmark_element(self, element, stream=None):
        if stream is None:
            stream = StringIO()
        if element.text:
            stream.write(element.text)
        for sub in element:
            self.unmark_element(sub, stream)
        if element.tail:
            stream.write(element.tail)
        return stream.getvalue()

    
    def _markdown_to_plaintxt(self, marked_txt):
        # patch Markdown
        Markdown.output_format["plain"] = self._unmark_element
        __md = Markdown(output_format="plain")
        __md.stripTopLevelTags = False
        # convert txt
        result = __md.convert(marked_txt)
        return result
        
    

### TESTING 
class TestSnippetSummary:
     def __init__(self):
        self.summarizer = AnnotationGeneration()
        print("Testing Snippet Summarizer... \n")
    
        #High-depth code is code that has many variables, refers to many functions, changes variables, and is overall complex to understand from a quick view
     def test_snippet_summarizer_from_high_depth_code(self):
          print("Testing code snippet summarizer with a high depth function... \n")
          code_snippet = '''
          const handleCreateEvent = async(e) => {
            e.preventDefault()
            // console.log(user)
            // const dateNow = new Date()
            // var date = JSON.stringify(dateNow.getFullYear()+'.'+(dateNow.getMonth()+1)+'.'+dateNow.getDate()).replace("\"", "").replace("\"", "");
                if (isDateRange == false){
                    await addDoc(collection(db, 'schools', completeSchoolName, 'events'), {
                      title: title,
                      description: description,
                      dateTime: dateTime,
                      location: location,
                      club: club,
                      dateAdded: Date().toLocaleString(),
                      // createdBy: {name: user.displayName, email: user.email}
                  }).then(setTitle("")).then(setDescription("")).then(setDateTime("")).then(setStartDateTime("")).then(setEndDateTime("")).then(setLocation("")).then(setClub("")).then(fetchUser())
                  
                  const chosenDate = new Date(dateTime)
                  var dateNow = new Date(chosenDate)
                  dateNow.setDate(chosenDate.getDate() + 1)
                  const date = JSON.stringify(dateNow.getFullYear()+'.'+(dateNow.getMonth()+1)+'.'+dateNow.getDate()).replace("\"", "").replace("\"", "")
                  await setDoc(doc(db, 'schools', completeSchoolName, 'announcements', date), {
                    notes: [{
                      title: title,
                      description: description,
                    club: club}],  
                    createdBy: {name: user.name, email: user.email},
                      dateAdded: Date().toLocaleString(),
                      // createdBy: {name: user.displayName, email: user.email}
                  }).then(setTitle("")).then(setDescription("")).then(setDateTime("")).then(setLocation("")).then(setClub("")).then(fetchUser())

                } else {
                  await addDoc(collection(db, 'schools', completeSchoolName, 'events'), {
                    title: title,
                    description: description,
                    startDate: startDateTime,
                    endDate: endDateTime,
                    location: location,
                    club: club,
                    dateAdded: Date().toLocaleString(),
                    // createdBy: {name: user.displayName, email: user.email}
                }).then(setTitle("")).then(setDescription("")).then(setDateTime("")).then(setStartDateTime("")).then(setEndDateTime("")).then(setLocation("")).then(setClub("")).then(fetchUser())
                
                const chosenDate = new Date(startDateTime)
                var dateNow = new Date(chosenDate)
                dateNow.setDate(chosenDate.getDate() + 1)
                const date = JSON.stringify(dateNow.getFullYear()+'.'+(dateNow.getMonth()+1)+'.'+dateNow.getDate()).replace("\"", "").replace("\"", "")
                await setDoc(doc(db, 'schools', completeSchoolName, 'announcements', date), {
                  notes: [{
                    title: title,
                    description: description,
                  club: club}],  
                  createdBy: {name: user.name, email: user.email},
                    dateAdded: Date().toLocaleString(),
                    // createdBy: {name: user.displayName, email: user.email}
                }).then(setTitle("")).then(setDescription("")).then(setDateTime("")).then(setLocation("")).then(setClub("")).then(fetchUser())

                }
                
      }'''
          output = self.summarizer.run(code_snippet)
          print(f"CODE SUMMARY: \n{output} \n\n")
          assert type(output) == str

          '''
          EXPECTED OUTPUT:The code is written in JavaScript, specifically using the async/await syntax to handle asynchronous operations with Firestore, a cloud database from Firebase. It defines an event-handling function `handleCreateEvent` meant to create and save event data into the Firestore database. When a form submission event triggers the function, it first prevents the default behavior with `e.preventDefault()`. 
          The function checks if `isDateRange` is false and, based on this, either adds or updates single or range-dated event documents in the Firestore under the 'events' collection. It also conditionally updates the 'announcements' collection based on the existence of date ranges. After database operations, it resets multiple state variables (title, description, dateTime, etc.) and fetches user data. 
          The function ensures newly created or modified data incorporates the current date and time and user metadata. The expected result includes adding appropriate entries in the Firestore under both 'events' and 'announcements' collections and resetting the form's state. 
          '''


     #Low-depth code is code that is fairly simple, not many variables, and easy to follow 
     def test_snippet_summarizer_from_low_depth_code(self):
          print("Testing code snippet summarizer with a low depth function... \n")
          code_snippet = '''
          class Solution:
            def topK(self, nums: List[int], k: int) -> List[int]:
                count = {}
                freq = [[] for i in range (len(nums) + 1)]
       
            for n in nums:
                count[n] = 1 + count.get(n, 0)
            for n, c in count.items():
                freq[c].append(n)
       
            res = []
       
            for i in range(len(freq) - 1, 0, -1):
                for n in freq[i]:
                    res.append(n)
                    if len(res) == k:
                        return res'''
          output = self.summarizer.run(code_snippet)
          print(f"CODE SUMMARY: \n{output} \n\n")
          assert type(output) == str
          '''
          EXPECTED OUTPUT:
          The code is written in Python and defines a method `topK` within a class `Solution`. The purpose of this method is to return the top k most frequent integers from a given list `nums`. 
          It first creates a `count` dictionary to tally the frequency of each number in `nums`, then organizes these frequencies into a list of lists `freq`. 
          The method then iterates through `freq` in reverse order to gather the k most frequent numbers into the result list `res`, which is returned once it reaches the desired length k. 
          '''
    

if __name__ == "__main__":
    TestSnippetSummary = TestSnippetSummary()
    TestSnippetSummary.test_snippet_summarizer_from_low_depth_code()
    TestSnippetSummary.test_snippet_summarizer_from_high_depth_code()

from openai import OpenAI

'''
Create a class to annotate a piece of given code
- input:
    - Code (Function, Class, etc.)
- output:
    - Summary of code in text
'''

class Annotation_Generation:
    def __init__(self):
        self.res = ""

    def snippet_summary(self, snippet):

            ## Set the API key
            client = OpenAI(api_key="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")

            MODEL="gpt-4o"

            completion = client.chat.completions.create(
            model=MODEL,
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

class TestSnippetSummary:
     def __init__(self):
        self.summarizer = Annotation_Generation()
        print("Testing Snippet Summarizer... \n")
     def test_snippet_summarizer_from_high_depth_code(self):
          print("Testing code snippet summarizer with a high depth function... \n")
          code_snippet = '''const handleCreateEvent = async(e) => {
        e.preventDefault()
        // console.log(user)
        // const dateNow = new Date()
        //         var date = JSON.stringify(dateNow.getFullYear()+'.'+(dateNow.getMonth()+1)+'.'+dateNow.getDate()).replace("\"", "").replace("\"", "");
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
          output = self.summarizer.snippet_summary(code_snippet)
          print(f"CODE SUMMARY: \n {output} \n\n")
          assert type(output) == str


     def test_snippet_summarizer_from_low_depth_code(self):
          print("Testing code snippet summarizer with a low depth function... \n")
          code_snippet = '''class Solution:
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
          output = self.summarizer.snippet_summary(code_snippet)
          print(f"CODE SUMMARY: \n {output} \n\n")
          assert type(output) == str
    
if __name__ == "__main__":
    TestSnippetSummary = TestSnippetSummary()
    TestSnippetSummary.test_snippet_summarizer_from_low_depth_code()
    TestSnippetSummary.test_snippet_summarizer_from_high_depth_code()
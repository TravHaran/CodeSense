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
        MODEL="gpt-3.5-turbo"

        completion = client.chat.completions.create(
        model=MODEL,
        #Prompt modelling, grounding the model to provide a more concise and clear summary when given a piece of code
        messages=[
            {"role": "system", "content": '''
            You are a developer assistant designed to provide detailed answers and assistance based on contextual explanations of code in a codebase. Your input consists of explanations of code files, their respective file directories, and file content within the codebase. Users will provide queries related to the codebase, seeking clarification, assistance, or suggestions. Your task is to utilize the provided context to generate clear and structured responses to the user queries. Your responses should be informative, accurate, and tailored to the specific query. Additionally, you may suggest potential actions or direct the user to relevant code files within the codebase for further reference. Your responses should solely rely on the provided context, avoiding external knowledge or assumptions. Remember to maintain clarity and coherence in your responses, ensuring that users can easily understand and follow your guidance. Make sure to keep your responses as short as possible as well so that the developer can quickly view an answer their question. Wrap any wrap any code examples in <code></code> blocks.
            DO NOT HAVE THE QUERY IN YOUR REPONSE

            Example:

            Query: How does the event-handling function handle errors during Firestore database operations?

            Context:
            The code is written in JavaScript, specifically using the async/await syntax to handle asynchronous operations with Firestore, a cloud database from Firebase. It defines an event-handling function `handleCreateEvent` meant to create and save event data into the Firestore database. When a form submission event triggers the function, it first prevents the default behavior with `e.preventDefault()`. The function checks if `isDateRange` is false and, based on this, either adds or updates single or range-dated event documents in the Firestore under the 'events' collection. It also conditionally updates the 'announcements' collection based on the existence of date ranges. After database operations, it resets multiple state variables (title, description, dateTime, etc.) and fetches user data. The function ensures newly created or modified data incorporates the current date and time and user metadata. The expected result includes adding appropriate entries in the Firestore under both 'events' and 'announcements' collections and resetting the form's state. 
            File Directory: NewsFlash/pages/events.js
            
            Content:
            import Head from 'next/head'
            import Image from 'next/image'
            import {auth, db} from '../firebase'
            import {useState, useEffect, Fragment} from 'react'
            import styles from '../styles/events.module.css'
            import { collection, getDocs, deleteDoc, doc, updateDoc, setDoc, addDoc, getDoc, get, getCountFromServer} from "firebase/firestore";
            import { useRouter } from 'next/router'
            import Event from '../components/event/event'
            import {signOut, onAuthStateChanged} from 'firebase/auth'

            const UpcomingEvents = () => {
                const router = useRouter()
                const [isAdmin, setIsAdmin] = useState(false)
                const [isLoggedIn, setIsLoggedIn] = useState(false)
                const [title, setTitle] = useState("")
                const [description, setDescription] = useState("")
                const [dateTime, setDateTime] = useState("")
                const [startDateTime, setStartDateTime] = useState("")
                const [endDateTime, setEndDateTime] = useState("")
                const [location, setLocation] = useState("")
                const [club, setClub] = useState("")
                const [completeSchoolName, setCompleteSchoolName] = useState("")
                const [eventsList, setEventsList] = useState([])
                const [eventsCount, setEventsCount] = useState(0)
                const [isTeacher, setIsTeacher] = useState(false)
                const [schoolName, setSchoolName] = useState("")
                const [schoolAbbrev, setSchoolAbbrev] = useState("")
                const [schoolId, setSchoolId] = useState("")
                const [loading, setLoading] = useState(true);
                const [user, setUser] = useState(null);
                const [refetch, setRefetch] = useState(false);
                const [isDateRange, setIsDateRange] = useState(false);
                const events = []
                const dateToday = new Date()
                const date = dateToday.toISOString().split('T')[0]
                const fetchUser = () => {
                // console.log({date})
                    onAuthStateChanged(auth, (user) => {
                    if (user) {
                        setIsLoggedIn(true)
                    
                    const fetch = async() => {
                        try{
                            const docRef = doc(db, "users", user.uid);
                            const docSnap = await getDoc(docRef);
                            if (docSnap.data().role == "teacher") {
                                setIsTeacher(true)
                                if (docSnap.data().admin) {
                                setIsAdmin(true)
                                }
                            }
                            if (docSnap.exists()) {
                            setUser(docSnap.data())
                                const collectionRef = collection(db, 'schools', docSnap.data().school_abbreviated+"_"+docSnap.data().school_id, 'events');
                                const snapshot = await getDocs(collectionRef);
                                const dataCount = await getCountFromServer(collectionRef)
                                snapshot.forEach(doc => {
                                    // console.log(doc.data())
                                    if (dataCount.data().count - 1 > events.length) {
                                        
                                        if (doc.data().__ == "__") {
                                        
                                        } else {
                                            const eventData = doc.data()
                                            eventData["id"] = doc.id
                                        events.push(eventData)
                                        }
                                    }
                                    setEventsList(events)
                                    // console.log(events)
                                    setEventsCount(dataCount.data().count - 1)
                                })
                            setSchoolName(docSnap.data().school_name)
                            setSchoolId(docSnap.data().school_id)
                            setSchoolAbbrev(docSnap.data().school_abbreviated)
                            setCompleteSchoolName(docSnap.data().school_abbreviated+"_"+docSnap.data().school_id)
                            // console.log(docSnap.data().school_abbreviated+"_"+docSnap.data().school_id)
                            setLoading(false)
                            } else {
                            setLoading(false)
                            router.replace("/login")
                            // console.log("No such document!");
                            }
                            } catch (err){
                            // console.log(err)
                            }
                    }
                    fetch()}
                    });
                    
                    
                }

                useEffect(() => {
                    fetchUser()
                }, [])
                useEffect(() => {
                    fetchUser()
                }, [refetch])

                const handleCreateEvent = async(e) => {
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
                            
                }
                return (
                    <div className={styles.container}>
                        <h1>Upcoming Events at {schoolAbbrev}</h1>
                        {isTeacher && 
                            <div className={styles.createContainer}>
                            <h3>Create Event</h3>
                            <form onSubmit={handleCreateEvent}>
                            <label>Title: </label>
                                <input required className={styles.inputs} value={title} onChange={(e) => {e.preventDefault(); setTitle(e.target.value)}}/>
                                <br />
                                <div className={styles.formTextArea}>
                                                <label>Description: </label>
                                <textarea className={styles.inputs}value={description} onChange={(e) => {e.preventDefault(); setDescription(e.target.value)}} />

                                </div>
                                <br />
                            {!isDateRange && (
                            <Fragment>
                                <label>Date: </label>
                                    <input type="date" required min={date} className={styles.inputs} value={dateTime} onChange={(e) => {e.preventDefault(); setDateTime(e.target.value);}} />
                                <br />
                            </Fragment>
                            ) 
                            }    
                            {isDateRange &&
                            <Fragment>
                                <label>Start Date: </label>
                                    <input type="date" required min={date} className={styles.inputs} value={startDateTime} onChange={(e) => {e.preventDefault(); setStartDateTime(e.target.value);}} />
                                <br />
                                <label>End Date: </label>
                                    <input type="date" required min={startDateTime} className={styles.inputs} value={endDateTime} onChange={(e) => {e.preventDefault(); setEndDateTime(e.target.value);}} />
                                <br />
                            </Fragment>
                            }
                                <label>Date Range: </label>
                                <input onChange={(e) => {setIsDateRange(e.target.checked)}} type="checkbox"/>
                                <br />
                            <label>Location: </label>
                                <input className={styles.inputs} value={location} onChange={(e) => {e.preventDefault(); setLocation(e.target.value)}} />
                                <br />
                            <label>Asscociated Club: </label>
                                <input className={styles.inputs} value={club} onChange={(e) => {e.preventDefault(); setClub(e.target.value)}} />
                            <button type="submit">Submit</button>
                            </form>
                            </div>
                            
                        }
                        <div className={styles.eventsContainer}>
                        {eventsList.map((event, idx) => {
                            return(
                                <div key={idx}>
                                    <Event 
                                    title={event.title} 
                                    setTitle={event.setTitle} 
                                    description={event.description}
                                    setDescription={event.setDescription}
                                    dateTime={event.dateTime}
                                    setDateTime={event.setDateTime}

                                    startDate={event.startDate ? event.startDate : null}
                                    endDate={event.endDate ? event.endDate : null}
                                    setStartDate={event.setStartDateTime}
                                    setEndDate={event.setEndDateTime}

                                    location={event.location}
                                    setLocation={event.setLocation}
                                    club={event.club}
                                    setClub={event.setClub}
                                    id={event.id}
                                    admin={isAdmin}
                                    completeSchoolName={completeSchoolName}
                                    setRefetch={setRefetch}
                                    refetch={refetch}
                                    />
                                </div>
                            )
                        })}

                        {
                            eventsList.length == 0 &&
                            <div className={styles.noAnnouncements}>
                            <h2>No Upcoming Events Yet.
                            </h2>
                            
                            </div>
                        }
                        </div>
                        
                        <br />
                        
                    </div>
                )
                }

            export default UpcomingEvents
            

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
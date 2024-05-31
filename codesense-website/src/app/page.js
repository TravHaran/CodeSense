"use client";


import { sendCodeBase, sendQuery, search, sendBatchCodeBase, sendBatchQuery, batchSearch } from './apiCalling';
import styles from './page.module.css'
import { Fragment, useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion';
import Modal from 'react-modal';
import Markdown from 'react-markdown'

// import Graph from 'react-json-graph';
// import test_codebase from '../../public/test_github_codebase.json'
// const fs = require("fs/promises");

export default function Home() {
  const [githubLink, setGithubLink] = useState("")
  const [isModelling, setIsModelling] = useState(false)
  const [codebase_modelled, set_codebase_modelled] = useState(false)
  const [query, setQuery] = useState("")
  const [querying, setQuerying] = useState(false)
  const [responseRecieved, setResponseRecieved] = useState(false)
  const [modalIsOpen, setIsOpen] = useState(false);
  const [ignoreFiles, setIgnoreFiles] = useState([]);
  const [ignoreFile, setIgnoreFile] = useState([]);
  const [repoList, setRepoList] = useState([]);
  const [notificationModal, setNotificationModal] = useState(false);
  const [notificationType, setNotificationType] = useState('error');
  const [notificationMessage, setNotificationMessage] = useState("Error");
  const [firstLink, setFirstLink] = useState("");
  const [codebaseJson, setCodebaseJson] = useState(null);
  const [response, setResponse] = useState("");
  const [completeResponse, setCompleteResponse] = useState(null);
  const [topResAnnotation, setTopResAnnotation] = useState(null);
  const [topResTitle, setTopResTitle] = useState(null);
  const [topResPath, setTopResPath] = useState(null);
  const [topRelevant, setTopRelevant] = useState(null);
  const [opacity, setOpacity] = useState(0);

  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

  var numOfPastSummaries = 0
  const pastSummaries = {'hey':'hey'}

  const customStyles = {
    content: {
      top: '50%',
      left: '50%',
      right: 'auto',
      bottom: 'auto',
      width: '70vw',
      marginRight: '-50%',
      transform: 'translate(-50%, -50%)',
      backgroundColor: 'black',
      borderRadius: '30px',
      padding: '6vh 5vw',
    },
    overlay: {
      backgroundColor: "rgb(0.49, 0.49, 0.49, 0.59)"
    }
  };


  function closeModal() {
    setIsOpen(false);
  }

  const handleSubmitQuery = async (query) => {
    if (query.length !== 0) {
      setQuerying(true)
    notification('positive', 'Querying Codebase...')
    console.log({repoList})
    if (repoList.length == 1) {
      var searchResponseData = await search(query, firstLink)
      var queryResponseData = await sendQuery(query, 5, firstLink)
    } else {
      var repositoryLists = new Set(repoList);
      setRepoList(Array.from(repositoryLists))
      console.log(query)
      console.log(repoList)
      const models = []
      repoList.forEach((item) => {
        models.push("https://github.com/"+item.path)
      }
      )
      console.log({"question": query, "limit": 5, "models": models})
      var queryResponseData = await sendBatchQuery(query, 5, models)
      var searchResponseData = await batchSearch(query, models)
    }
    var queryResponse = JSON.parse(queryResponseData)
    var searchResponse = JSON.parse(searchResponseData)
    // var queryResponse = queryResponseData
    
    console.log({searchResponse})
    setCompleteResponse(queryResponse)
    setResponse(queryResponse.answer)
    setTopRelevant(searchResponse)
      localStorage.setItem('completeResponse', JSON.stringify(queryResponse))
      localStorage.setItem('response_text', queryResponse.answer)
      localStorage.setItem('top_relevant', JSON.stringify(searchResponse))
      setResponseRecieved(true)
      setQuerying(false)
      notification('positive', 'Response Generated!')
    } else {
      notification('error', 'Error: Please input a query before continuing')
    }
  }

  

  useEffect(() => {
    if (repoList.length > 0) {
      setFirstLink(repoList[0].path)
      console.log(repoList[0])
    }
  }, [repoList])

  const handleSubmit = async () => {
    // console.log(repositoryList)
    
    if (repoList.length == 0 && githubLink == "") {
      notification('error', "Error: Please enter a Github Repository link before continuing")
    } else {
      var repositoryLists = new Set(repoList);
      setRepoList(Array.from(repositoryLists))
      await handleAddRepo()
      setIsModelling(true);
    set_codebase_modelled(false)
    notification('positive', 'Codebase Modelling in progress..')
    localStorage.setItem('githubLinks', (JSON.stringify(repoList)))
    localStorage.setItem('ignoreFiles', ignoreFiles)
      const repositoryList = repoList
    if (repositoryList.length <= 1) {
      console.log(firstLink)
      var codebase_modelled = await sendCodeBase(githubLink == "" ? firstLink : githubLink, [])
    notification('positive', 'Codebase Sucessfully Modelled!')
    localStorage.setItem('modelled_codebase', codebase_modelled)
    } else if (repositoryList.length > 1) {
      var codebase_modelled = await sendBatchCodeBase(repoList)
      console.log(codebase_modelled)
    notification('positive', 'Codebase Sucessfully Modelled!')
    localStorage.setItem('modelled_codebase', codebase_modelled)
    }
    
    setIsModelling(false)
    set_codebase_modelled(true);
    }
    
    
  };


  const handleRestart = () => {
    setGithubLink("")
    localStorage.removeItem('githubLinks')
    localStorage.removeItem('ignoreFiles')
    localStorage.removeItem('modelled_codebase')
    localStorage.removeItem('completeResponse')
    localStorage.removeItem('top_relevant')
    localStorage.removeItem('response_text')
    setRepoList([])
    setIsModelling(false)
    set_codebase_modelled(false)
    setIgnoreFiles([])
    setQuery("")
    setQuerying(false)
    setResponseRecieved(false)
  }

  useEffect(() => {
    if (localStorage.getItem("modelled_codebase")) {
      console.log(JSON.parse(localStorage.getItem("modelled_codebase")))
      const codeBase = JSON.parse(localStorage.getItem("modelled_codebase"))
      if ('results' in codeBase) {
       var repoListBatch = []
        codeBase.results.forEach((item) => {
          repoListBatch.push({path: item.name, ignore: []})
        })
        localStorage.setItem("githubLinks", JSON.stringify(repoListBatch))
      } else {
        localStorage.setItem("githubLinks", JSON.stringify([{path: codeBase.name, ignore: []}]))
      }
      set_codebase_modelled(true)
      
      const repositoryList = JSON.parse(localStorage.getItem("githubLinks"))
      setRepoList(repositoryList)
      console.log(repositoryList)
      setCodebaseJson(JSON.parse(localStorage.getItem("modelled_codebase")))
    } else {
      console.log('none')
      // handleRestart()
    }
    if (localStorage.getItem("completeResponse")) {
      setCompleteResponse(JSON.parse(localStorage.getItem("complete_response")))
    setResponse(localStorage.getItem("response_text"))
    setQuery(JSON.parse(localStorage.getItem("completeResponse")).question)
    setTopRelevant(JSON.parse(localStorage.getItem("top_relevant")))
    setResponseRecieved(true)
    setQuerying(false)
    }
  }, [])

  useEffect(() => {
    if (responseRecieved) {
      setQuerying(false)
    }
  }, [responseRecieved])

  function allStorage() {
    for (var i = 0; i<localStorage.length; i++) {
        pastSummaries[i] = localStorage.getItem(localStorage.key(i));
        numOfPastSummaries += 1
    }
  }
  useEffect(() => {
    allStorage() 
  }, [modalIsOpen])

  const handleAddRepo = async () => {
    if (githubLink !== "") {
      if (githubLink.includes("github.com/") && githubLink.split('/').length == 5) {
        setRepoList(repoList => [...repoList, {"path": githubLink, ignore: ignoreFiles}])
      } else {
        notification('error', 'Error: Please enter a Github repository link')
      }
      
    } else if (repoList.length==0) {
      notification('error', "Error: Please enter a Github Repository link before continuing")
    }
    setGithubLink("")
    setIgnoreFiles([])
  }

  const handleAddIgnoreFile = () => {
    if (ignoreFile.length !== 0) {
      setIgnoreFiles(() => ([...ignoreFiles, ignoreFile]))
      setIgnoreFile("")
    }
    else if  (ignoreFile.length == 0){
      notification('error', 'Error: No file added')
    }
  }

  const notification = (type, message) => {
    if (notificationModal == true) {
      setNotificationModal(false)
    }
    setNotificationType(type)
    setNotificationMessage(message)
    setNotificationModal(true)
    setTimeout(function(){
      setNotificationModal(false);
  }, 100);
    
  }


      

  return (
    <div className={styles.container} >
      <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />
      <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />
      <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />
      <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />
      <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />
    <div className={styles.titleSmall}>
      <motion.button transition={{duration: 0.4}} whileHover={{scale: 1.1, color: '#C41E3A'}} whileTap={{scale: 0.9}} className={styles.restart} onClick={(e) => {e.preventDefault(); handleRestart()}}><span class="material-symbols-outlined">
exit_to_app
</span></motion.button>
    <h1 className={styles.title}>Codesense</h1>
    <motion.div style={{ left: -30 }} animate={codebase_modelled ? {scale:0.5, height:'100px'} : {}} className={codebase_modelled ? styles.inputContainerSmall : styles.inputContainer}>
    {!localStorage.getItem('githubLinks') ? (
      <Fragment><div className={styles.repoListContainer}>
          
        </div>
        <div className={styles.repoContainer}>
          <div className={styles.addedRepoContainer}>
            {repoList.map(repo => 
              <li>{repo.path}</li>
            )}
          </div>
          
            <div className={styles.mainInputAndButton}>
              {!isModelling &&
              <motion.button whileHover={{scale: 1.1}} whileTap={{scale: 0.9}} onClick={handleAddRepo} className={styles.addRepository}><span class="material-symbols-outlined">add</span></motion.button>
              }
              
          <form onSubmit={(e) => {e.preventDefault(); handleAddRepo()}}>
          <input
              type="url"
              value={githubLink}
              id="book"
              className={styles.bookInput}
              autoFocus
              disabled={isModelling ? true : false}
              onChange={(e) => {setGithubLink(e.target.value);}}
              placeholder="Enter Github URL"
            />
            
            </form>
            {!isModelling &&
            <motion.button whileHover={{scale: 1.1}} whileTap={{scale: 0.9}} onClick={async(e) => {
            e.preventDefault(); 
            if (repoList.length == 0) {
              await handleAddRepo()
            }
            handleSubmit()}} className={styles.submitRepo}><span class="material-symbols-outlined">
arrow_forward_ios
</span></motion.button>
            }
            
            </div>
          
            
        </div>
        
          
            <form onSubmit={(e) => {e.preventDefault(); handleAddIgnoreFile()}}>
              <h3 className={styles.ignoreHeader}>Ignore Files List</h3>
              <div className={styles.ignoreFilesList}>
                {ignoreFiles.map(file =>
    <li>{file}</li>
  )}
              </div>
            
              <input className={styles.ignoreInput} value={ignoreFile} onChange={(e)=> {setIgnoreFile(e.target.value)}} placeholder="Name of File"/>
            <button onClick={(e) => {e.preventDefault(); handleAddIgnoreFile()}} className={styles.buttonStyle}>Add</button>
              </form>
             {/* <Graph
    width={600}
    height={400}
    json={codebaseJson}
    onChange={(newGraphJSON) => {}}
/>  */}
      </Fragment>
         
    ): (
      <div className={styles.topRepoList}>
{repoList.map(repo => 
          <p
          className={styles.topRepoInput}
          style={{background:'none'}}
          >
          <b>PROJECT:</b> {("https://github.com/"+repo.path).split('/').pop().replaceAll("-", " ")}
          <br />
          <b>OWNER:</b> {(("https://github.com/"+repo.path)).split('/')[3]}<br />
          <b>Link:</b> <a className={styles.pathLink} href={"https://github.com/"+repo.path} target='_blank'>{"https://github.com/"+repo.path}</a></p>
          
        )
        }
      
    </div>
    )}
    {modalIsOpen && 
    <motion.div
    initial={{scale: 0.5}} 
    transition={{duration: 0.9}} 
    animate={{scale: 1}}>
<Modal
    isOpen={modalIsOpen}
    
    onRequestClose={closeModal}
    style={customStyles}
    closeTimeoutMS={200}
    ariaHideApp={false}>
          <h1>{topResTitle}</h1>
          <b>Path:</b> <p className={styles.pathLink}><a href={topResPath} target="_blank">{topResPath}</a></p>
          <div>
            <hr /><br /><h4>File Summary:</h4><b></b> <Markdown className={styles.fileAnnotation} >{topResAnnotation}</Markdown>
          </div>
          
          
          
    </Modal>

</motion.div>}

    
    </motion.div>
    
    </div>
    {codebase_modelled && 
        <div className={!querying ? styles.inputContainer : styles.responseContainer}>
          {!responseRecieved &&
          <p className={styles.enterQuestion}><b>ENTER CODEBASE QUERY: </b></p>
          }<form onSubmit={(e) => {e.preventDefault(); handleSubmitQuery(query)}}>
            <div className={styles.queryContainer}>
<div className={styles.queryInputContainer}>
<textarea id="query" disabled={ querying ? true : false || responseRecieved ? true : false} className={!responseRecieved ? styles.queryInputBefore : styles.queryInputAfter} onChange={(e) => {setQuery(e.target.value);}} value={query}/>

            </div>
            {!querying && !responseRecieved &&
            <motion.button initial={{scale: 0.5}} 
            transition={{duration: 0.2}} 
            whileHover={{scale: 1.1}}
            whileTap={{scale: 0.9}}
            animate={{scale: 1}} className={styles.submitQueryButton} type='submit'><span class="material-symbols-outlined">
            search
            </span></motion.button>
            }
            
            </div>
            
          {responseRecieved &&
          <motion.button initial={{y: 100}} whileHover={{scale: 1.1}} whileTap={{scale:0.9}} transition={{duration: 0.1}} animate={{y: 0}} className={styles.newQuestionButton} onClick={() => {setQuery(""); setQuerying(false); setResponseRecieved(false); setTimeout(function(){
            document.getElementById("query").focus()
        }, 2000);}}><span class="material-symbols-outlined">
        restart_alt
        </span></motion.button>
          }</form>
          
          {responseRecieved &&
          <div className={styles.gptResponseContainer}>
            <div className={styles.response}>
              <div className={styles.progressiveText}>
              {/* <Typewriter words={[response]} deleteSpeed={0} typeSpeed={1} /> */}
                <Markdown className={styles.responseText} >{response}</Markdown>
              </div>
              
            </div>
            
            <div className={styles.topFilesContainer}>
              <h3 className={styles.topFilesTitle}>Most Relevant Files</h3>
              <hr />
              <br />
              <div className={styles.topFilesListContainer}>
                <ol>
{
                topRelevant.results.map((item) =>
                <motion.li initial={{y: 100}} whileHover={{scale: 1.1}} whileTap={{scale:0.9}} transition={{duration: 0.01}} animate={{y: 0}} onClick={() => {setIsOpen(true);
                  setTopResAnnotation(item.highlights);
                  setTopResTitle(item.node.name); 
                  setTopResPath(item.node.link)
                  setTimeout(() => {
                    setOpacity(1);
                  }, 100);
                }}
                className={styles.topFile}>{item.node.name}</motion.li>
                )
              }
                  
                </ol>
                
              </div>
              
            </div>
          </div>
          }
          
      </div>
      
    }
    {isModelling &&
      <div>
      <progress className={styles.loading}></progress>
      </div>
    }
    {querying &&
      <div>
      <progress className={styles.loading}></progress>
      </div>
    }
    <AnimatePresence>
    {notificationModal &&
      <motion.div 
      transition={{duration: 2}}
      initial={{ opacity: 0.7}}
      animate={{ opacity: 1}}
      exit={{ display: 'none'}}
      >
        <h3 className={notificationType == "error" ? styles.error : styles.positive}>{notificationMessage}</h3>
      </motion.div>
    }
    </AnimatePresence>
    
  </div>
  )
}
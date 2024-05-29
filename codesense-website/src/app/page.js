"use client";

import Head from 'next/head'
import Image from 'next/image'
import styles from './page.module.css'
import { Fragment, useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion';
import Modal from 'react-modal';
import bg from '../../public/background.jpeg'
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
  const [codebaseJson, setCodebaseJson] = useState(null);
  const [response, setResponse] = useState("");

  var numOfPastSummaries = 0
  const pastSummaries = {'hey':'hey'}

  const customStyles = {
    content: {
      top: '50%',
      left: '50%',
      right: 'auto',
      bottom: 'auto',
      marginRight: '-50%',
      transform: 'translate(-50%, -50%)',
    },
  };


  function closeModal() {
    setIsOpen(false);
  }

  const handleSubmitQuery = async (query) => {
    if (query.length !== 0) {
      setQuerying(true)
    notification('positive', 'Querying Codebase...')


    setResponse("To add a \"square\" function to the existing \"Calc\" struct in \"calc.rs\", you would define a new method called \"square\" in the \"impl\" block. This function will take a \"Vec<f64>\" and return a new \"Vec<f64>\" where each element is the square of the corresponding element in the input vector. Additionally, you will need to add a test case for this new function in the \"test_all_operations\" function.")

    setTimeout(function(){
      setResponseRecieved(true)
      setQuerying(false)
      notification('positive', 'Response Generated!')
  }, 2000);
    } else {
      notification('error', 'Error: Please input a query before continuing')
    }
  }

  const handleSubmit = async () => {

    if (githubLink !== "") {
      if (githubLink.includes("github.com/")) {
        setRepoList(repoList => [...repoList, githubLink])
        console.log(repoList)
      } else {
        notification('error', 'Error: Please enter a Github repository link')
      }
    }
    const repositoryList = repoList
    if (repositoryList.length == 0 && githubLink == "") {
      handleRestart
      // notification('error', "Error: Please enter a Github Repository link before continuing")
    } else {
      setIsModelling(true);
    set_codebase_modelled(false)
    notification('positive', 'Codebase Modelling in progress..')
localStorage.setItem('githubLinks', JSON.stringify(repoList))
    localStorage.setItem('ignoreFiles', ignoreFiles)
    const bookTitleAndAuthor = JSON.stringify({
      githubLink
    })
    console.log(bookTitleAndAuthor)
    
    const res = await fetch("/api/createMessage", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: bookTitleAndAuthor,
    });
    setTimeout(function(){
      notification('positive', 'Codebase Modelling Completed!')
  }, 2000);
    

    setTimeout(function(){
      setIsModelling(false); 
      set_codebase_modelled(true)
  }, 5000);
    
    
    
    // console.log("RES: "+res.status)
    // if (!res.ok) {
    //   throw new Error(`HTTP error! status: ${res.status}`);
    // }
    // const data = await res.json();
    // // console.log("MESSAGE: "+data.bookSummary)
    // } catch (err) {
    //   console.error('An error occurred while fetching the data.', err)
    // }
    }
    
    
  };


  const handleRestart = () => {
    setGithubLink("")
    localStorage.removeItem('githubLinks')
    localStorage.removeItem('ignoreFiles')
    setRepoList([])
    set_codebase_modelled(false)
    setIgnoreFiles([])
    setQuery("")
    setQuerying(false)
    setResponseRecieved(false)
  }

  useEffect(() => {
    if (localStorage.getItem("githubLinks") && JSON.parse(localStorage.getItem("githubLinks").length !== 2)) {
      set_codebase_modelled(true)
      setRepoList(JSON.parse(localStorage.getItem("githubLinks")))
      console.log(JSON.parse(localStorage.getItem("githubLinks").length))
    } else {
      console.log('none')
      handleRestart()
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
        setRepoList(repoList => [...repoList, githubLink])
      } else {
        notification('error', 'Error: Please enter a Github repository link')
      }
      
    } else {
      notification('error', "Error: Please enter a Github Repository link before continuing")
    }
    setGithubLink("")
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
    <div className={styles.container} style={{
      backgroundImage: `url(${bg.src})`,
    }}>
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
              <li>{repo}</li>
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
            <motion.button whileHover={{scale: 1.1}} whileTap={{scale: 0.9}} onClick={(e) => {e.preventDefault(); handleSubmit()}} className={styles.submitRepo}><span class="material-symbols-outlined">
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
          <b>PROJECT:</b> {repo.split('/').pop().replaceAll("-", " ")}
          <br />
          <b>OWNER:</b> {repo.split('/')[3]}<br />
          <b>Link:</b> <a href={repo} target='_blank'>{repo}</a></p>
          
        )
        }
      
    </div>
    )}

    <Modal
    isOpen={modalIsOpen}
    onRequestClose={closeModal}
    style={customStyles}
    ariaHideApp={false}>
          <h1>Past Summaries</h1>
          <div>
            <p>hey</p>
            
          </div>
          
          
          
    </Modal>
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
            <button className={styles.submitQueryButton} type='submit'><span class="material-symbols-outlined">
arrow_forward_ios
</span></button>
            }
            
            </div>
            
          {responseRecieved &&
          <button className={styles.newQuestionButton} onClick={() => {setQuery(""); setQuerying(false); setResponseRecieved(false); setTimeout(function(){
            document.getElementById("query").focus()
        }, 2000);}}><span class="material-symbols-outlined">
        restart_alt
        </span></button>
          }</form>
          {responseRecieved &&
          <div className={styles.responseContainer}>
<div className={styles.response}>
            <p  id="response">{response}</p>
              
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
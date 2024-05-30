"use client";

import Head from 'next/head'
import Image from 'next/image'
import { sendCodeBase, sendQuery } from './apiCalling';
import styles from './page.module.css'
import { Fragment, useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion';
import Modal from 'react-modal';
import bg from '../../public/background.jpeg'
import axios from 'axios';
import MarkdownView from 'react-showdown';

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
    var queryResponseData = await sendQuery(query, 5, firstLink)
   
    var queryResponse = JSON.parse(queryResponseData).answer
    
    console.log(queryResponse)
    setResponse(queryResponse)

    setTimeout(function(){
      setResponseRecieved(true)
      setQuerying(false)
      notification('positive', 'Response Generated!')
  }, 2000);
    } else {
      notification('error', 'Error: Please input a query before continuing')
    }
  }

  useEffect(() => {
    if (repoList.length > 0) {
      setFirstLink(repoList[0].path)
      console.log(repoList[0].path)
    }
  }, [repoList])

  const handleSubmit = async () => {
    if (githubLink !== "") {
      await handleAddRepo()
    }
    // console.log(repositoryList)
    if (repoList.length == 0 && githubLink == "") {
      notification('error', "Error: Please enter a Github Repository link before continuing")
    } else {
      setIsModelling(true);
    set_codebase_modelled(false)
    notification('positive', 'Codebase Modelling in progress..')
    localStorage.setItem('githubLinks', JSON.stringify(repoList))
    localStorage.setItem('ignoreFiles', ignoreFiles)
      const repositoryList = repoList
    if (repositoryList.length <= 1) {
      console.log(firstLink)
      var codebase_modelled = await sendCodeBase(githubLink == "" ? firstLink : githubLink, [])
    notification('positive', 'Codebase Sucessfully Modelled!')
    localStorage.setItem('modelled_codebase', codebase_modelled)
    } else if (repositoryList.length > 1) {
      console.log('repoList')
      var codebase_modelled = await sendCodeBase(repoList[0].path, [])
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
    setRepoList([])
    setIsModelling(false)
    set_codebase_modelled(false)
    setIgnoreFiles([])
    setQuery("")
    setQuerying(false)
    setResponseRecieved(false)
  }

  useEffect(() => {
    if (localStorage.getItem("modelled_codebase") && JSON.parse(localStorage.getItem("githubLinks").length !== 2)) {
      set_codebase_modelled(true)
      setRepoList(JSON.parse(localStorage.getItem("githubLinks")))
      setCodebaseJson(JSON.parse(localStorage.getItem("modelled_codebase")))
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
        setRepoList(repoList => [...repoList, {"path": githubLink, ignore: ignoreFiles}])
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
          <b>PROJECT:</b> {repo.path.split('/').pop().replaceAll("-", " ")}
          <br />
          <b>OWNER:</b> {repo.path.split('/')[3]}<br />
          <b>Link:</b> <a href={repo.path} target='_blank'>{repo.path}</a></p>
          
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
<MarkdownView className={styles.response} markdown={response} />
              
          
          
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
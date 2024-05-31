'use server'
import axios from 'axios';

export async function sendCodeBase(path, ignore){
    return new Promise((resolve, reject) => {
    let data = JSON.stringify({
        path,
        ignore
      });
      
      let config = {
        method: 'post',
        maxBodyLength: Infinity,
        url: 'http://127.0.0.1:8000/model',
        headers: { 
          'Content-Type': 'application/json',
          "Access-Control-Allow-Origin": "*",
"Access-Control-Allow-Headers": "Origin, Content-Type, Accept"
        },
        data : data
      };
      
      var res = axios.request(config).then(res => {resolve(JSON.stringify(res.data))})
    
      })      

    
}
export async function sendBatchCodeBase(paths){
    return new Promise((resolve, reject) => {
    let data = JSON.stringify({
        "models": paths
      });
      
      let config = {
        method: 'post',
        maxBodyLength: Infinity,
        url: 'http://127.0.0.1:8000/batchModel',
        headers: { 
          'Content-Type': 'application/json',
          "Access-Control-Allow-Origin": "*",
"Access-Control-Allow-Headers": "Origin, Content-Type, Accept"
        },
        data : data
      };
      
      var res = axios.request(config).then(res => {resolve(JSON.stringify(res.data))})
    
      })      

    
}

export async function sendBatchQuery(question, limit, models){
    return new Promise((resolve, reject) => {
        let data = JSON.stringify({
            question,
            limit,
            models
        });
          
          let config = {
            method: 'get',
            maxBodyLength: Infinity,
            url: 'http://127.0.0.1:8000/batchQuery',
            headers: { 
              'Content-Type': 'application/json'
            },
            data : data
          };
          
      var res = axios.request(config).then(res => {resolve(JSON.stringify(res.data))}, (error) => {console.log(error)})
    
      })      

    
}

export async function sendQuery(question, limit, path){
    return new Promise((resolve, reject) => {
        let data = JSON.stringify({
            question,
            limit,
            path
          });
          
          let config = {
            method: 'get',
            maxBodyLength: Infinity,
            url: 'http://127.0.0.1:8000/query',
            headers: { 
              'Content-Type': 'application/json'
            },
            data : data
          };
      var res = axios.request(config).then(res => {resolve(JSON.stringify(res.data))})
    
      })      

    
}

export async function search(question, path){
    return new Promise((resolve, reject) => {
        let data = JSON.stringify({
            question,
            path
          });
          
          let config = {
            method: 'get',
            maxBodyLength: Infinity,
            url: 'http://127.0.0.1:8000/search',
            headers: { 
              'Content-Type': 'application/json'
            },
            data : data
          };
      var res = axios.request(config).then((res) => {resolve(JSON.stringify(res.data))}, (error) => {console.log(error)})
    //   console.log(res)
    
      })      

    
}
export async function batchSearch(question, paths){
    return new Promise((resolve, reject) => {
        let data = JSON.stringify({
            question,
            "models": paths
        });
          
          let config = {
            method: 'get',
            maxBodyLength: Infinity,
            url: 'http://127.0.0.1:8000/batchSearch',
            headers: { 
              'Content-Type': 'application/json'
            },
            data : data
          };
      var res = axios.request(config).then(res => {resolve(JSON.stringify(res.data))})
    
      })      

    
}
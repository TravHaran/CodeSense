from fastapi import FastAPI, Query, HTTPException, Path, Request, HTTPException
from models import ModelRequest, BatchModelRequest, QueryRequest, BatchQueryRequest
from typing import Optional, List
import json 
from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel

import sys
sys.path.insert(0, "..")
from app import App 
import logging
from codebase_extract.github_codebase_extract import CodeBaseExtractGithub
from multithreading.batch_model import BatchModel
from multithreading.batch_query import BatchQuery
from utilities.utility import json_to_obj, obj_to_json

app = FastAPI()
logging.basicConfig(level=logging.DEBUG)

@app.post('/model')
async def model(request: ModelRequest):
    codebase_path = request.path
    extractor = CodeBaseExtractGithub(codebase_path)
    repo_owner = extractor.owner
    repo_name = extractor.repo_name
    print(codebase_path)
    ignores = request.ignore
    print(ignores)
    response = App().model_code_base(codebase_path, ignores)
    # save model
    save_file_name = f"{repo_owner}_{repo_name}"
    obj_to_json("database/models", save_file_name, response)
    return response

@app.post('/batchModel')
async def batchModel(request: BatchModelRequest):
    model_requests = request.models
    codebase_paths = ""
    for entry in model_requests:
        path = entry.path
        extractor = CodeBaseExtractGithub(path)
        repo_owner = extractor.owner
        repo_name = extractor.repo_name
        codebase_paths += f"{repo_owner}_{repo_name}"
    response = BatchModel(model_requests).run()
    # save batch models
    save_file_name = f"{codebase_paths}"
    obj_to_json("database/batch_models", save_file_name, response)
    return response

@app.get('/search')
async def search(request: SearchRequest):
    codebase_path = request.path
    question = request.question
    
    extractor = CodeBaseExtractGithub(codebase_path)
    repo_owner = extractor.owner
    repo_name = extractor.repo_name
    model_name = f"{repo_owner}_{repo_name}"
    # get model
    model = json_to_obj(f"database/models/{model_name}.json")
    response = App().search_code_base(model, question)
    now = str(datetime.now())
    # save response
    save_file_name = f"query_response_{now}"
    obj_to_json("database/queries", save_file_name, response)
    return response
    
    

@app.get('/query')
async def query(request: QueryRequest):
    codebase_path = request.path
    question = request.question
    limit = request.limit
    
    extractor = CodeBaseExtractGithub(codebase_path)
    repo_owner = extractor.owner
    repo_name = extractor.repo_name
    model_name = f"{repo_owner}_{repo_name}"
    # get model
    model = json_to_obj(f"database/models/{model_name}.json")
    response = App().query_code_base(model, question, limit)
    now = str(datetime.now())
    # save response
    save_file_name = f"query_response_{now}"
    obj_to_json("database/queries", save_file_name, response)
    return response

@app.get('/batchQuery')
async def batchQuery(request: BatchQueryRequest):
    codebases = request.models
    batch_models = ""
    for path in codebases:
        extractor = CodeBaseExtractGithub(path)
        repo_owner = extractor.owner
        repo_name = extractor.repo_name
        model_name = f"{repo_owner}_{repo_name}"
        batch_models += model_name
    question = request.question
    limit = request.limit
    # get models
    models = json_to_obj(f"database/batch_models/{batch_models}.json")
    response = BatchQuery(models, question, limit).run()
    # save response
    now = str(datetime.now())
    save_file_name = f"batch_query_request_{now}"
    obj_to_json("../out", save_file_name, response)
    return response
    

    
    
    


    
    
    
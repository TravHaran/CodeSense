from fastapi import FastAPI, Query, HTTPException, Path
from models import ModelRequest, BatchModelRequest, QueryRequest, BatchQueryRequest
from typing import Optional, List
import json 
from datetime import datetime

import sys
sys.path.insert(0, "..")
from app import App 
from multithreading.batch_model import BatchModel
from multithreading.batch_query import BatchQuery
from utilities.utility import obj_to_json

app = FastAPI()

@app.get('/model')
def model(request: ModelRequest):
    codebase_path = request.path
    print(codebase_path)
    ignores = request.ignore
    print(ignores)
    codebase_model = App().model_code_base(codebase_path, ignores)
    now = str(datetime.now())
    save_file_name = f"model_request_{now}"
    obj_to_json("../out", save_file_name, codebase_model)
    return codebase_model

@app.get('/batchModel')
def batchModel(request: BatchModelRequest):
    model_requests = request.models
    codebase_models = BatchModel(model_requests).run()
    now = str(datetime.now())
    save_file_name = f"batch_model_request_{now}"
    obj_to_json("../out", save_file_name, codebase_models)
    return codebase_models

@app.get('/query')
def query(request: QueryRequest):
    codebase_model = request.model
    question = request.question
    limit = request.limit
    response = App().query_code_base(codebase_model, question, limit)
    now = str(datetime.now())
    save_file_name = f"query_request_{now}"
    obj_to_json("../out", save_file_name, response)
    return response

@app.get('/batchQuery')
def batchQuery(request: BatchQueryRequest):
    codebase_models = request.batch_models
    question = request.question
    limit = request.limit
    response = BatchQuery(codebase_models, question, limit).run()
    now = str(datetime.now())
    save_file_name = f"batch_query_request_{now}"
    obj_to_json("../out", save_file_name, response)
    return response
    
    
    
    
    


    
    
    
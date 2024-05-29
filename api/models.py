from pydantic import BaseModel

class ModelRequest(BaseModel):
    path: str
    ignore: list[str] = []

class CodebaseModel(BaseModel):
    name: str
    path: str
    type: str
    keywords: list[str]
    children: list = []


class BatchModelRequest(BaseModel):
    models: list[ModelRequest]

class BatchModelResponse(BaseModel):
    results: list[CodebaseModel]

class QueryRequest(BaseModel):
    question: str
    limit: int
    model: CodebaseModel

class BatchQueryRequest(BaseModel):
    question: str
    limit: int
    batch_models: BatchModelResponse
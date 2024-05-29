from pydantic import BaseModel

class ModelRequest(BaseModel):
    path: str
    ignore: list[str] = []
    def __getitem__(self, item):
        return getattr(self, item)

class BatchModelRequest(BaseModel):
    models: list[ModelRequest] 


class QueryRequest(BaseModel):
    question: str
    limit: int
    path: str

class BatchQueryRequest(BaseModel):
    question: str
    limit: int
    models: list[str] = []
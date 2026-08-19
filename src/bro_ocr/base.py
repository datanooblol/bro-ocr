from pydantic import BaseModel, Field
from typing import List
from enum import StrEnum

class Dtype(StrEnum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"

class Schema(BaseModel):
    field:str
    dtype:Dtype
    instruction:str

class Patch(BaseModel):
    x:int
    y:int
    w:int
    h:int
    schemas:List[Schema]

class Template(BaseModel):
    name:str
    instruction:str
    width:int
    height:int
    patches:List[Patch]
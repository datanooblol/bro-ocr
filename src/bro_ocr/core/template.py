from pydantic import BaseModel, Field
from typing import List, Optional
from enum import StrEnum

class Dtype(StrEnum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"

class Schema(BaseModel):
    """This serves as instruction for information extraction"""
    field:str = Field(description="This is a field name")
    dtype:Dtype = Field(description="dtype is an enum of Dtype")
    instruction:Optional[str] = Field(description="instruction here will be applied only with in this field only", default=None)

class Patch(BaseModel):
    """Patch is a region of interest inside an image"""
    x:int
    y:int
    w:int
    h:int
    schemas:List[Schema] = Field(description="One patch can have more than one schema")

class Template(BaseModel):
    name:str
    instruction:Optional[str] = Field(description="this is a global instruction that will apply to all patches", default=None)
    width:int = Field(description="this is an image's width")
    height:int = Field(description="this is an image's height")
    patches:List[Patch] = Field(description="a collection of Patch")
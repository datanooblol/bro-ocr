from bro_ocr.core.template import Schema
from pydantic import create_model
from typing import List

DTYPE_MAP = dict(
    string=str,
    integer=int,
    float=float,
    boolean=bool,
    date=str,
    datetime=str
)

class SchemaConverter:
    @staticmethod
    def _get_params(schemas:List[Schema]):
        params = {}
        for s in schemas:
            params[s.field] = (DTYPE_MAP[s.dtype])
        return params

    @classmethod
    def from_single(cls, name, schemas:List[Schema]):
        if len(schemas) != 1:
            raise ValueError("single schema must have exactly one schema")
        params = cls._get_params(schemas)
        return create_model(name, **params)

    @classmethod
    def from_object(cls, name, schemas:List[Schema]):
        if not (len(schemas) > 1):
            raise ValueError("object schema must have more than one schema")
        params = cls._get_params(schemas)
        schema = create_model(f"{name}_model",**params)
        params = {f"{name}":schema}
        return create_model(name, **params)

    @classmethod
    def from_list(cls, name:str, schemas:List[Schema]):
        params = cls._get_params(schemas)
        schema = create_model(f"{name}_model",**params)
        params = {f"{name}":List[schema]}
        return create_model(name, **params)
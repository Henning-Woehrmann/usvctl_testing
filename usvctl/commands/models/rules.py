from __future__ import annotations
from typing import Dict, List
from pydantic import BaseModel
import httpx

from ...exceptions import handle_api_response


class Selectors(BaseModel):
    matchLabels: Dict = dict()


class Condition(BaseModel):
    soc: int


class Metadata(BaseModel):
    name: str
    labels: Dict = dict()


class Spec(BaseModel):
    enabled: bool = False
    selectors: Selectors
    condition: Condition


class Rule(BaseModel):
    kind: str = "Rule"
    metadata: Metadata
    spec: Spec

    @classmethod
    def get(cls, api_address: str, name: str) -> Rule:
        response = httpx.get(f"{api_address}/rule/{name}")
        handle_api_response(response)
        return cls.parse_raw(response.content)

    def delete(self, api_address: str):
        response = httpx.delete(f"{api_address}/rule/{self.metadata.name}")

        handle_api_response(response)

    def create(self, api_address: str):
        response = httpx.post(f"{api_address}/rule", data=self.json())

        handle_api_response(response)

    def update(self, api_address: str):
        response = httpx.patch(f"{api_address}/rule/{self.metadata.name}", data=self.json())

        handle_api_response(response)


class Rules(BaseModel):
    __root__: List[Rule]

    @classmethod
    def get(cls, api_address: str) -> Rules:
        response = httpx.get(f"{api_address}/rules")
        handle_api_response(response)
        return cls.parse_raw(response.content)

    def create():
        ...

    def delete():
        ...

    def update():
        ...

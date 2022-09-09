from __future__ import annotations
from typing import Dict, List
from pydantic import BaseModel
import httpx

from ...exceptions import handle_api_response


class Metadata(BaseModel):
    name: str
    labels: Dict = dict()


class Spec(BaseModel):
    enabled: bool = False
    endpoint: str
    action: str
    test: str = ""
    healthcheck: str = ""


class Task(BaseModel):
    kind: str = "Task"
    metadata: Metadata
    spec: Spec

    @classmethod
    def get(cls, api_address: str, name: str) -> Task:
        response = httpx.get(f"{api_address}/task/{name}")
        handle_api_response(response)
        return cls.parse_raw(response.content)

    def delete(self, api_address: str):
        response = httpx.delete(f"{api_address}/task/{self.metadata.name}")

        handle_api_response(response)

    def create(self, api_address: str):
        response = httpx.post(f"{api_address}/task", data=self.json())

        handle_api_response(response)

    def update(self, api_address: str):
        response = httpx.patch(f"{api_address}/task/{self.metadata.name}", data=self.json())

        handle_api_response(response)


class Tasks(BaseModel):
    __root__: List[Task]

    @classmethod
    def get(cls, api_address: str) -> Tasks:
        response = httpx.get(f"{api_address}/tasks")
        handle_api_response(response)
        return cls.parse_raw(response.content)

    def create():
        ...

    def delete():
        ...

    def update():
        ...

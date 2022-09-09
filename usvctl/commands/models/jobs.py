from __future__ import annotations
from typing import List
from pydantic import BaseModel
import httpx

from ...exceptions import handle_api_response


class Labels(BaseModel):
    task: str
    rule: str


class Metadata(BaseModel):
    uuid: str
    labels: Labels

class Status(BaseModel):
    enabled: bool
    state: str
    rule_enabled: bool
    task_enabled: bool


class Job(BaseModel):
    kind: str
    metadata: Metadata
    status: Status


class Jobs(BaseModel):
    __root__: List[Job]

    @classmethod
    def get(cls, api_address: str) -> Jobs:
        response = httpx.get(f"{api_address}/jobs")
        handle_api_response(response)
        return cls.parse_raw(response.content)

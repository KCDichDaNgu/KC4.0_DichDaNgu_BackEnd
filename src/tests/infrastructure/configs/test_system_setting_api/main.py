from pathlib import Path
from pydantic import Field, BaseSettings, BaseModel

from typing import Any, Dict, Optional, Union
from enum import unique

from pydantic.networks import AnyHttpUrl
from umongo.frameworks import MotorAsyncIOInstance, PyMongoInstance
from core.types import ExtendedEnum

from infrastructure.configs.database import CassandraDatabase, MongoDBDatabase
from infrastructure.configs.event_dispatcher import KafkaConsumer, KafkaProducer

import os

import requests
import json
from jsonschema import validate
from jsonschema import Draft6Validator

schema = {
    "$schema": "https://json-schema.org/schema#",

    "type" : "object",
    "properties" : {
        "status" : {"type" : "string"},
        "setting": {
            "type": "object",
            "properties": {
                "path": { "type": "string" },
                "name": { "type": "string" },
                "summary": {
                    "anyOf": [
                        {"type": "string"},
                        {"type": "null"}
                    ] },
                "desc": {
                    "anyOf": [
                        {"type": "string"},
                        {"type": "null"}
                    ] },
                "method": {
                    "anyOf": [
                        {"type": "string"},
                        {"type": "null"}
                    ] },
                "abstract": {"type": "bool"}
            },
            "required": ["path", "name", "abstract"]
        }
    }
}

def test_system_setting_check_status_code_equals_200():
    response = requests.get("http://demo.example.com/setting/case1")
    assert response.status_code == 200

def test_system_setting_validates_json_resonse_schema():
    response = requests.get("http://demo.example.com/setting")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    resp_body = response.json()
    validate(instance=resp_body, schema=schema)

def test_system_setting_negative_call():
    response = requests.get("http://demo.example.com/setting/case2")
    assert response.status_code == 200

def test_system_setting_destruction():
    response = requests.get("http://demo.example.com/setting")
    assert response.status_code == 200

def main():
    test_system_setting_check_status_code_equals_200()
    test_system_setting_validates_json_resonse_schema()
    test_system_setting_negative_call()
    test_system_setting_destruction()
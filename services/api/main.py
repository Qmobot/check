#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=no-name-in-module

__author__ = "Bauyrzhan Ospan"
__copyright__ = "Copyright 2021"
__version__ = "1.0.1"

import telebot
from telebot import types
from typing import Optional
from fastapi import FastAPI, Form, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from random import randint, choice, randrange
from datetime import datetime, timedelta
import copy
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
import gunicorn
import uvloop
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from pymongo import MongoClient
import pymongo
import logging

path = os.getcwd()
os.environ['TZ'] = 'Asia/Almaty'
logging.error("API started again")

# region: Database
class Database:
    def __init__(self):
        self.client = MongoClient('mongodb://database:27017/')

        self.db = self.client["qmobot"]
        self.checks = self.db['checks']



DB = Database()

# endregion

# region: Create app and CORS

app = FastAPI(
    title="OceanMind project documentation for MasterHubs",
    description="This is documentation for developers",
    version="2.1.0"
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# endregion


# region: Talking to real masterhub methods

@app.get("/checks/{data}")
async def check(data: str, request: Request):
    logging.error(data)
    client_host = request.client.host
    logging.error(client_host)
    DB.checks.insert_one({"name": data, "ip": client_host})
    return "ok"


# endregion

if __name__ == "__main__":
	uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True, workers=4)

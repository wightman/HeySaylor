#!/usr/bin/env python3 
import datetime
from enum import Enum
from typing import List
import pymysql.cursors
from pymysql.err import MySQLError
import requests
import uvicorn
from fastapi import FastAPI, Response, HTTPException
from pydantic import BaseModel

import settings

app = FastAPI()

#  SIGNAL CRUD

# MODELS ##########

# # A signal tuple
class Signal(BaseModel):
    signalId: int
    description: str

class URL(BaseModel):
    url: str


# signals Resource Collection Endpoint ##########

@app.post("/signals/", response_model=URL)
def addSignal(signal: Signal):
    sql = 'addSignal'
    sqlargs = (signal.signalId, signal.description)
    try:
        dbConnection = pymysql.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_DATABASE,
            charset='utf8mb4',
            cursorclass= pymysql.cursors.DictCursor)
        cursor = dbConnection.cursor()
        cursor.callproc(sql, sqlargs) # stored procedure, no arguments
        row = cursor.fetchone()
        dbConnection.commit()
        cursor.close()
    except MySQLError as e:
        oops = str(e.args[1]+" ("+str(e.args[0])+")" )
        raise HTTPException(status_code=500, detail=oops)
    finally:
        dbConnection.close()
    uri = 'http://'+settings.APP_HOST+':'+str(settings.APP_PORT)
    uri = uri+'/signals'+'/'+str(row['sigId'])
    return { "url": uri }

@app.get("/signals/", response_model=List[Signal])
def getSignals():
    sql = 'getSignals'
    try:
        dbConnection = pymysql.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_DATABASE,
            charset='utf8mb4',
            cursorclass= pymysql.cursors.DictCursor)
        cursor = dbConnection.cursor()
        cursor.callproc(sql) # stored procedure, no arguments
        rows = cursor.fetchall() # get all the results
        cursor.close()
    except MySQLError as e:
        oops = str(e.args[1]+" ("+e.args[0]+")" )
        raise HTTPException(status_code=500, detail=oops)
    finally:
        dbConnection.close()
    return rows # turn set into json and return it


# signals Individual Resource Endpoint ##########

@app.get("/signals/{signal_id}", response_model=Signal)
def getSignal(signal_id : int):
    sql = 'getSignal'
    sqlArgs = (signal_id,)
    try:
        dbConnection = pymysql.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_DATABASE,
            charset='utf8mb4',
            cursorclass= pymysql.cursors.DictCursor)
        cursor = dbConnection.cursor()
        cursor.callproc(sql,sqlArgs) # stored procedure,  arguments
        row = cursor.fetchone() # get the results
        cursor.close()
    except MySQLError as e:
        oops = str(e.args[1]+" ("+str(e.args[0])+")" )
        raise HTTPException(status_code=500, detail=oops)
    finally:
        dbConnection.close()
    return row # turn set into json and return it

@app.put("/signals/{signal_id}", response_model=None)
def addSignal(signal: Signal):
    sql = 'updateSignal'
    sqlargs = (signal.signalId, signal.description)
    try:
        dbConnection = pymysql.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_DATABASE,
            charset='utf8mb4',
            cursorclass= pymysql.cursors.DictCursor)
        cursor = dbConnection.cursor()
        cursor.callproc(sql, sqlargs) # stored procedure, no arguments
        dbConnection.commit()
        cursor.close()
    except MySQLError as e:
        oops = str(e.args[1]+" ("+str(e.args[0])+")" )
        raise HTTPException(status_code=500, detail=oops)
    finally:
        dbConnection.close()
    return 

if __name__ == "__main__":
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)

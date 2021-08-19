#
# app/api.py
# 
import os, glob
from datetime import  date, time, datetime, timedelta
from typing import Tuple, Optional, Any

from fastapi import FastAPI, Depends, Response, HTTPException
from fastapi import File, Form, UploadFile
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from pydantic import BaseModel

from fastapi_sessions.backends import InMemoryBackend
from fastapi_sessions import SessionCookie, SessionInfo
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.responses import RedirectResponse
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware


from app.models import User
from app.models import SaylorPost, Saylor
from app.auth import get_password_hash, dbCheckCredentials, loggedIn
from app.dbAccess import dbAccess
import app.settings as settings

## Big rocks
# 
app = FastAPI()
security = HTTPBasic()
app.add_middleware(HTTPSRedirectMiddleware)

## CORS overrides for development
#
#if settings.APP_DEV:
#    from fastapi.middleware.cors import CORSMiddleware
#    origins = [
#        "http://localhost"
#    ]
#
#    app.add_middleware(
#        CORSMiddleware,
#        allow_origins=origins,
#        allow_credentials=True,
#        allow_methods=["*"],
#        allow_headers=["*"],
#    )
#    print("Accepting origins: ", origins)

## Session things
#
session = SessionCookie(
    name="hey_saylor",
    secret_key=settings.SECRET_KEY,
    data_model=User,
    backend=InMemoryBackend(),
    auto_error=False
)
## SPA Client
#
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
app.mount("/js", StaticFiles(directory="static/js", html=True), name="static")
app.mount("/css", StaticFiles(directory="static/css", html=True), name="static")
app.mount("/img", StaticFiles(directory="static/img", html=True), name="static")
@app.get("/")
async def redirect():#
    response = RedirectResponse(url='/static')
    return response
@app.get('/favicon.ico')
async def favicon():
    file_name = "favicon.ico"
    file_path = os.path.join(app.root_path, "static")
    return FileResponse(path=file_path, headers={"Content-Disposition": "attachment; filename=" + file_name})

###############################################################################
# Endpoints
#

## /sessions: POST, DELETE
#

# curl -i --insecure --user 'wightman@unb.ca:J0lly R0g3r!' -X 'POST' \
#  -c cookie_jar 'http://127.0.0.1:8000/sessions' \
#  -H 'accept: application/json' \
#  -d ''
#
@app.post("/sessions", status_code=201)
async def login(response: Response, session_info: Optional[SessionInfo] = Depends(session),
    credentials: HTTPBasicCredentials = Depends(security)):

    old_session = None
    if session_info:
        old_session = session_info[0]

    emailCredential = credentials.username
    pwCredential = credentials.password
    userSession = dbCheckCredentials(emailCredential, get_password_hash(pwCredential) ) 
    
    await session.create_session(userSession, response, old_session)

    return userSession

# curl -X DELETE --insecure -b cookie_jar 'http://127.0.0.1:8000/sessions'
#
@app.delete("/sessions", status_code=204)
async def logout(response: Response, session_info: Optional[SessionInfo]  = Depends(session)):
    #print (session_info)
    loggedIn(session_info)
    await session.end_session(session_info[0], response)
    return {"message": "Logged out"}

## /saylors: POST, GET
#
@app.post("/saylors", status_code=201)
async def createSaylor(saylor_post: SaylorPost, session_info: Optional[SessionInfo]  = Depends(session)):
    loggedIn(session_info)
    # saylor data from json
    sqlProc = 'postSaylor'
    sqlArgs = ()
    return {"message": "createSaylor"}

# curl -X GET --insecure -b cookie_jar 'http://127.0.0.1:8000/saylors'
#
@app.get("/saylors")
async def getSaylors(session_info: Optional[SessionInfo]  = Depends(session)):
    loggedIn(session_info)
    sqlProc = 'getSaylorsComponent'
    sqlArgs = ()
    saylors = dbAccess(sqlProc, sqlArgs)
    return saylors

## /saylors/{saylorId}: get, update, delete
#
# curl -X GET --insecure -b cookie_jar 'http://127.0.0.1:8000/saylors/3'
#
@app.get("/saylors/{saylor_id}")
async def getSaylor(saylor_id: int, session_info: Optional[SessionInfo]  = Depends(session)):
    loggedIn(session_info)
    sqlProc = 'getSaylor'
    sqlArgs = (saylor_id,)
    saylor = dbAccess(sqlProc, sqlArgs)
    return saylor

@app.put("/saylors/{saylor_id}", status_code=204)
async def putSaylor(saylor_id: int, saylor_update: Saylor, session_info: Optional[SessionInfo]  = Depends(session) ):
    loggedIn(session_info)
    # saylor data from json
    sqlProc = 'putSaylor'
    sqlArgs = ()

    return {"message": "putSaylor"}

@app.delete("/saylors/{saylor_id}", status_code=204)
async def deleteSaylors(saylor_id: int, session_info: Optional[SessionInfo]  = Depends(session)):
    loggedIn(session_info)
    sqlProc = 'deleteSaylor'
    sqlArgs = (saylor_id)
    return {"message": "deleteSaylor"}

## /saylors/{saylorId}/wills/{willNo}: get, update, delete
#
#  Management of wills as a weak entity of saylors. Wills are stored as pdfs on
#   the file system (in pwd/wills), named in the form lastName-firstName-SaylorId-WillNo.pdf

willPath = os.getcwd()
willPath = os.path.join(willPath,"docs")
willPath = os.path.join(willPath,"wills")

# curl -X GET --insecure -b cookie_jar 'http://127.0.0.1:8000/saylors/3/wills/1'
#
@app.get("/saylors/{saylor_id}/wills/{willNo}")
async def getSaylorWill(saylor_id: int, willNo: int):
    files = "*-"+str(saylor_id)+"-"+str(willNo)+".pdf"
    filePath = os.path.join(willPath,files)
    wills = glob.glob(filePath)
    # should be only one!
    if len(wills) == 1:
        #normal
        return FileResponse(wills[0], media_type="application/pdf")
    else:
        #weirdness
        raise HTTPException(
            status_code=400,
            detail="Unable to find unique will"
        )

#curl -i --insecure  -X 'POST' \
#  -b cookie_jar 'https://0.0.0.0:8000/saylors/3/wills' \
#  -F 'dateOfWill=1962-12-27'\
#  -F 'documentName=Wightman-Rick-3-1.pdf'\
#  -F 'fileb=@./Wightman-Rick-3-1.pdf'\
#  -H 'Content-Type: multipart/form-data'

@app.post("/saylors/{saylor_id}/wills")
async def postSaylorWill(saylor_id: int,
    fileb: UploadFile = File(...),
    documentName: str = Form(...),
    dateOfWill: date = Form(...),
    notes: Optional[str] = Form(None),
    session_info: Optional[SessionInfo] = Depends(session), status_code=201):
    # willNum is 1 - only first wills can be uploaded
    # token should hold the form data : documentName, dateOfWill, notes, userId
    # fileb is the actual pdf
    #
    loggedIn(session_info)
    user = session_info[1]
    createdBy = user.userId
    # Steps of development:
    # 4. add will record.

    filename = os.path.join(willPath, documentName)
    # Does it exist? Quit
    if os.path.exists(filename):
        return ({
            "status" : "error",
            "message": "File exists"
        })
    try:
        f = open(filename, 'wb')
        content = await file.read()
    except Exception as e:
        if hasattr(e, 'message'):
            return ({
                "status" : "error",
                "message": e.message
            })
    try:
        f.write(content)
    except Exception as e:
        if hasattr(e, 'message'):
            return ({
                "status" : "error",
                "message": e.message
            })    
    finally:
        f.close()
    #4.
    sqlProc = 'addWill'
    sqlArgs = (saylor_id, 1, documentName, dateOfWill, notes, createdBy)
    try:
        dbAccess(sqlProc, sqlArgs)
    except Exception as e:
        if hasattr(e, 'message'):
            return ({
                "status" : "error",
                "message": e.message
            })
    # We're done!
    return {"status": "success"}

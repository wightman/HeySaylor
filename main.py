#!/usr/bin/env python3
# main.py

import uvicorn
from app.settings import APP_HOST, APP_PORT, APP_CERT, APP_KEY, APP_DEV

if __name__ == "__main__":
    uvicorn.run("app.api:app", 
        host=APP_HOST, 
        port=APP_PORT, 
        ssl_keyfile=APP_KEY, 
        ssl_certfile=APP_CERT
    )

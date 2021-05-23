#
# Authorization stuff
#
import pymysql
import bcrypt
from fastapi import HTTPException
import app.settings as settings

## Cryptography 
#
def get_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), salt=settings.PW_SALT.encode('utf-8'))

def dbCheckCredentials(uName: str, uPass: str):
    sqlProc = 'checkCredentials'
    sqlArgs = (uName, uPass)
    try:
        dbConnection = pymysql.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_DATABASE,
            charset='utf8mb4',
            cursorclass= pymysql.cursors.DictCursor)
        cursor = dbConnection.cursor()
        cursor.callproc(sqlProc, sqlArgs) # stored procedure, two arguments
        rows = cursor.fetchall()
        cursor.close()
    except pymysql.MySQLError as e:
        # if not (correct_username or correct_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        ) 
    finally:
        #close dbConnection
        if 'dbConnection' in locals():
            dbConnection.close()
    return rows[0]

def loggedIn(session_data):
    if session_data is None:
        raise HTTPException(
            status_code=403,
            detail="Not authenticated"
        )


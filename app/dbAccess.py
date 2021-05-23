import pymysql
from fastapi import HTTPException
import app.settings as settings
# 
# POST - specify object, return new Id
# GET(s) - no argument, return rows
# GET - Id, return row
# PUT - Id, Object, no return
# DELETE - Id, no return
def dbAccess(sqlProc: str, sqlArgs: tuple):
    try:
        dbConnection = pymysql.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_DATABASE,
            charset='utf8mb4',
            cursorclass= pymysql.cursors.DictCursor)
    except pymysql.MySQLError as e:
        raise HTTPException(
            status_code=500,
            detail="Could not connect to database"
        )
    try:
        cursor = dbConnection.cursor()
        cursor.callproc(sqlProc, sqlArgs)
        rows = cursor.fetchall()
        dbConnection.commit()
        cursor.close()
    except pymysql.MySQLError as e:
        raise HTTPException(
            status_code=500,
            detail="Database Error:"+str(e)
        ) 
    finally:
        dbConnection.commit()
        dbConnection.close()
    if len(rows) == 0:
        return
    return rows

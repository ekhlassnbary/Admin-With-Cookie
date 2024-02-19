from fastapi import FastAPI, HTTPException, Cookie, Response, Request, security
import mysql.connector
from starlette.responses import RedirectResponse
from cryptography.fernet import Fernet

# encrypted_userid = cipher.encrypt(results[0][0].encode()).decode()

#
app = FastAPI()
encryption_key = b'BpthmmKROjL-bMMnZD8h-jye-ZJN6cY7z-QB3ms_qD0='


# Initialize the Fernet cipher with the encryption key
cipher = Fernet(encryption_key)


#

# Connect to MySQL database
connection = mysql.connector.connect(
    host='localhost',
    database='usersandpass',
    user='root',
    password='root')

# Middleware to protect routes
@app.middleware("http")
async def authentication_middleware(request: Request, call_next):
    if request.url.path.startswith("/admin"):
        userid = request.cookies.get("UserId")
        if not userid:
            return RedirectResponse(url="/login")
        else:
            check_admin(userid)
    response = await call_next(request)
    return response




@app.get("/Login")
def name(username:str,password:str, response: Response):
    """
    log in with username and password and
    if the user in my db i do cookie and
    save userid init

    """
    cursor = connection.cursor()
    query = 'SELECT UserId FROM admin WHERE UserId = %s and UserPassword=%s'
    cursor.execute(query, (username,password))
    results = cursor.fetchall()
    cursor.close()

    if results:
        encrypted_userid = cipher.encrypt(results[0][0].encode())
        response.set_cookie(key="UserId", value=encrypted_userid)
        return {"message": "Login successful"}
    else:
            raise HTTPException(status_code=401, detail="Unauthorized")
    return {"message": "Please login"}





# def iscookie(UserId: str = Cookie(None)):
#     """"
#     check if the userid in cookie
#     """
#     if UserId:
#             return {"message": f'You have longed in before ,welcome {UserId}'}
#     raise HTTPException(status_code=401, detail="Unauthorized")
#
#


@app.get("/admin")
def check_admin(UserId: str = Cookie(None)):
    user=cipher.decrypt(eval(UserId)).decode()
    return {"message": f'You have longed in before ,welcome {user}'}

#
#
#
#
#
@app.get("/login")
async def login():
    # Implement your login logic here
    return {"message": "Please login"}

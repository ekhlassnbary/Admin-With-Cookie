from fastapi import FastAPI, HTTPException, Cookie, Response, Request
from starlette.responses import RedirectResponse, HTMLResponse
from cryptography.fernet import Fernet
from fastapi import FastAPI, UploadFile, Form, HTTPException
from typing import Annotated
from fastapi.responses import HTMLResponse
from starlette.responses import JSONResponse
import os
import mysql.connector
import boto3

app = FastAPI()
encryption_key = b'BpthmmKROjL-bMMnZD8h-jye-ZJN6cY7z-QB3ms_qD0='
cipher = Fernet(encryption_key)

# Connect to MySQL database
connection = mysql.connector.connect(
    host='localhost',
    database='last',
    user='root',
    password='root')

@app.middleware("http")
async def authentication_middleware(request: Request, call_next):
    if request.url.path.startswith("/admin"):
        userid = request.cookies.get("name")
        print(userid)
        if userid is None:
            return RedirectResponse(url="/Login")
        else:
            return await call_next(request)
    else:
        response = await call_next(request)
        return response
   

@app.get("/admin")
async def admin(request:Request):
        response = RedirectResponse(url="/upload")  # Redirect to /upload route
        return response


@app.get("/Login")
async def login(name: str, password: str, response: Response):
    """
    Login with username and password.
    If the user exists in the database, set a cookie with their encrypted id and redirect to the upload page.
    """
    cursor = connection.cursor()
    query = 'SELECT id FROM customer WHERE name = %s and password = %s'
    cursor.execute(query, (name, password))
    results = cursor.fetchall()
    cursor.close()

    if results:
        # Encrypt UserID and set it as a cookie
        encrypted_userid = cipher.encrypt(str(results[0][0]).encode()).decode()
        response=RedirectResponse(url="/upload")  # Redirect to /upload route

        response.set_cookie(key="name", value=encrypted_userid)
        # RedirectResponse(url="/upload")  # Redirect to /upload route
        return response
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/upload", response_class=HTMLResponse)
async def get_upload_form():
    """
    Endpoint to render the upload form.
    """
    html_content = """
       <html>
       <head>
           <title>Upload Image</title>
       </head>
       <body>
           <h1 style="text-align: center">Upload Image</h1>
           <form style="text-align: center; margin-left: 20px; margin-right: 20px; padding: 12px; border: 2px solid black; border-color: red;" action="/uploadtos3" method="post" enctype="multipart/form-data">
               <label for="name">Name:</label>
               <input type="text" placeholder="Enter Name" name="namee" required><br><br>
               <label for="image">Select image:</label>
               <input type="file" id="image" name="file" accept=".jpg, .jpeg, .png, .gif" required><br><br>
               <button type="submit">Upload</button>
           </form>
       </body>
       </html>
       """
    return HTMLResponse(content=html_content, status_code=200)


s3 = boto3.client('s3',
                  aws_access_key_id='AKIAVRUVWTPOIEDMWTD4',
                  aws_secret_access_key='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',
                  region_name='us-east-1'
                  )





@app.post("/uploadtos3")
async def up_to_s3(request: Request, namee: str = Form(...), file: UploadFile = UploadFile(...)):
    # Read the contents of the uploaded file
    contents = await file.read()
    filename, file_extension = os.path.splitext(file.filename)

    # Define the new filename
    new_filename = f"{namee}{file_extension}"  # Change the filename as desired
    file_path = os.path.join("assetes/", new_filename)

    # Save the file locally
    with open(file_path, "wb") as new_file:
        new_file.write(contents)

    # Upload the file to S3
    bucket_name = 'testaplouad'
    object_name = f'destination/{new_filename}'  # Specify the desired destination path in the S3 bucket
    region_name = 'us-east-1'  # Optional, specify if your bucket is in a region other than the default one

    s3.upload_file(file_path, bucket_name, object_name)

    # Get the URL of the uploaded file
    file_url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"

    # Get the user ID from the cookie
    userid = request.cookies.get("name")
    userid_=cipher.decrypt((userid)).decode()
    print(userid_)
    # Update the database with the file path
    return await addpathtodb(userid, file_url)

async def addpathtodb(id, path):
    
    try:
        cursor = connection.cursor()
        query = 'UPDATE customer SET file_path = %s WHERE id= %s'
        userid=cipher.decrypt((id)).decode()
        print(userid)
        cursor.execute(query, (path, userid))
        connection.commit()  # Commit the transaction
        cursor.close()
        return "Upload successful"
    except Exception as e:
        # Print or log the error message
        print(f"Error updating database: {e}")
        # Rollback the transaction if an error occurs
        connection.rollback()
        return "Error updating database"
    



@app.get("/abc")
async def saints(request: Request):
    cursor = connection.cursor()
    query = 'SELECT * FROM customer WHERE id = %s'
    userid = request.cookies.get("name")
    userid_ = cipher.decrypt(userid.encode()).decode()
    cursor.execute(query, (userid_,))
    html_user = "<div>User details:</div>"
    for row in cursor.fetchall():
        html_user += "<div>"
        html_user += f"<p>id= {row[0]}  </p>"
        html_user += f"<p>name= {row[1]}  </p>"
        html_user += f"<p>age= {row[2]}  </p>"
        html_user += f"<p>occubation= {row[3]}  </p>"
        html_user += f'<img src="{row[4]}"/>'

        html_user += "</div>"
    return HTMLResponse(content=html_user)

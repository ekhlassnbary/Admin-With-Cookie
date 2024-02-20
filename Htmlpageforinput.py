
from fastapi import FastAPI, UploadFile,Form, Query,HTTPException
import json
from typing import Annotated

from fastapi import FastAPI, File, UploadFile,Request


app = FastAPI()
from starlette.responses import HTMLResponse, JSONResponse

@app.get("/upload", response_class=HTMLResponse)
async def get_upload_form():
    html_content = """
       <html>
       <head>
           <title>Upload Image</title>
       </head>
       <body>
           <h1 style="text-align: center">Upload Image</h1>
           <form style="text-align: center; margin-left: 20px; margin-right: 20px; padding: 12px; border: 2px solid black; border-color: red;" action="/up" method="post" enctype="multipart/form-data">
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


import os

@app.post("/up")
async def up_to_assets(namee: str = Form(...), file: UploadFile = UploadFile(...)):
    # Read the contents of the uploaded file
    contents = await file.read()
    filename, file_extension = os.path.splitext(file.filename)

    # Define the new filename
    new_filename = f"{namee}{file_extension}"  # Change the filename as desired




    # Ensure the directory exists, create it if it doesn't
    os.makedirs("assetes/", exist_ok=True)

    # Define the path for the new file
    file_path = os.path.join("assetes/",new_filename)

    # Save the file with the new filename
    with open(file_path, "wb") as new_file:
        new_file.write(contents)


    return {"filename": new_filename, "name": namee}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)


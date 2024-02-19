from fastapi import FastAPI, File, UploadFile, Query,HTTPException
import json
import os

from starlette.responses import HTMLResponse, JSONResponse

with open('customer.json', 'r+') as file:
        content = json.load(file)



app = FastAPI()


@app.get("/")
async def index():
    return "Ahalan! You can fetch some json by navigating to '/json'"

@app.get("/json")
async def jsonc():
    return content

#
@app.get("/saints")
async def saints():
    filew=[]
    for item in content:
        if item.get("occupation", {}).get("isSaint", True):
            filew.append(item)

    return filew


#
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8001)


# Add another route
#    /short-desc
#    Which will send back only the customers names and occupations.
@app.get("/short-desc")
def short_desc():
    filew=[]
    for item in content:
            filew.append([item["name"],item["occupation"]])
    return filew



# 4- Add another route
#    /who?name=abraham
#    (This is called: query parameter)
#    This route will send back only the given customer (name=rachel will send back 'No such customer')
#    (If you change to /who?name=miryam and hit enter, Miryam data should be shown)
@app.get("/who")
async def whoname(name: str):
    for item in content:
        if item["name"].lower() == name.lower():
            return item
    return "'No such customer'"





# Update /saints
#    /saints?isSaint=true
#    Which will return saints or not saints, depending on the query parameter
@app.get("/saintsup")
async def saints_update(isSaint:bool):
    filew=[]
    for item in content:
        if item["occupation"]["isSaint"]==isSaint:
            filew.append(item)
    return filew


# Add another ability to /saints route - POST request.
#    When sending a new saint object to this route using POST http method - add the new saint to the json file.
#    Don't expect to get the new id - The server is responsible for that!
#    *Use Postman (install if needed)
#
# @app.post("/saintsAdd")
# async def saints_Add(object:dict):
#
#     with open('customer.json', 'r') as file:
#         content = json.load(file)
#
#     content.append(object)
#
#     with open('customer.json', 'w') as file:
#         json.dump(content, file, indent=4)
#
#     return content


# Return HTML page with simple display of the customers (table or just divs)
#    (Read about HTML response)

@app.get("/customers", response_class=HTMLResponse)
async def get_customers():
    html_content = "<h1>Customer Information</h1>"
    html_content += "<table border='1'><tr><th>ID</th><th>Name</th><th>Age</th><th>Occupation</th></tr>"

    for user in content:

        html_content += (f"<tr><td>{user['id']}</td><td>{user['name']}</td><td>{user['age']}</td><td>"
                     f"{user['occupation']['name']} ({'Saint' if user['occupation']['isSaint'] else 
                     'Non-Saint'})</td></tr>")
    html_content += "</table>"
    return html_content








# @app.post("/saints")
# async def saints_(object: dict):
#     with open(file_path, 'w+') as file:
#         content = file.read()
#
#     content.append(object)
#             # file.truncate()
#
#     return data
#
#

# 9
@app.get("/rewho")
async def Refer_get_name(name: str = Query(..., min_length=2, max_length=11)):

    for item in content:
     if item["name"].lower() == name.lower():
                return item

#
#
#
#


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)



# 8
# Make the customer name is linkable,
#      So when clicking a name - navigate to your existing routing (/who)!
@app.get("/jsonName")
async def linkable_name():

    html_content = "<html><body>"
    for item in content:
        linked_name = f'<a href=who?name={item["name"]}>{item["name"]}</a>'
        item["name"] = linked_name
        item_json = json.dumps(item)
        html_content += item_json + "<br>"
    html_content += "</body></html>"

    return HTMLResponse(content=html_content)





# 10
# done









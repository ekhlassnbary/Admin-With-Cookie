import mysql.connector
from fastapi import FastAPI, HTTPException

# Connect to the MySQL database
connection = mysql.connector.connect(
    host='localhost',
    database='last',
    user='root',
    password='root'
)

app = FastAPI()

@app.post("/items")
def create_item(item: dict):
        cursor = connection.cursor()
        query_occubation = "INSERT INTO occupation  (name, is_saint) VALUES (%s, %s)"
        cursor.execute(query_occubation, (item["occupation"]["name"], item["occupation"]["isSaint"]))
        connection.commit()
        occupation_id = cursor.lastrowid
        query_customer = "INSERT INTO customer (id, name, age, occupation_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(query_customer, (item["id"], item["name"], item["age"], occupation_id))
        connection.commit()

        cursor.close()

        return ("messageItem created successfully")



# 14- Expose those routings:
#     /admin/saint/age/10/130 - returns saints aged between 10 and 130 years.
#     /admin/notsaint/age/10/130 - returns not saints aged between 10 and 130 years.
#     /admin/name/ra - returns saints with name containing ra
#     /admin/average - returns the average ages of saints and not saints.



@app.get("/admin/saint/age/{fromm}/{to}")
def age(fromm:int,to:int):
        cursor = connection.cursor()
        query = f'SELECT * FROM customer JOIN occupation ON occupation.id = customer.occupation_id WHERE age BETWEEN {fromm} AND {to} AND is_saint = true'
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results



@app.get("/admin/notsaint/age/{fromm}/{to}")
def age_not(fromm:int,to:int):
        cursor = connection.cursor()
        query = f'SELECT * FROM customer JOIN occupation ON occupation.id = customer.occupation_id WHERE age BETWEEN {fromm} AND {to} AND is_saint = false'
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results




@app.get("/admin/name/{re}")
def contain(re:str):
        cursor = connection.cursor()
        query = f"SELECT * FROM customer JOIN occupation ON occupation.id = customer.occupation_id WHERE customer.name like '%{re}%'"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results

@app.get("/admin/average")
def avg():
        cursor = connection.cursor()
        query = "SELECT avg(age) FROM customer"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results

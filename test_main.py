from fastapi.testclient import TestClient
from main import app
file_path = 'customers.json'
import json
client = TestClient(app)




def test_json():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() =="Ahalan! You can fetch some json by navigating to '/json'"


def test_jsonc():
    response = client.get("/json")
    assert response.status_code == 200
    with open('customer.json', 'r') as file:
        content = file.read()

    assert response.json() ==json.loads(content)





saintsTrue=[
    {
        "id": 2,
        "name": "Sara",
        "age": 90,
        "occupation": {
            "name": "Our Mother",
            "isSaint": True
        }
    },
    {
        "id": 3,
        "name": "Yakov",
        "age": 110,
        "occupation": {
            "name": "Our 3rd Father",
            "isSaint": True
        }
    },
    {
        "id": 4,
        "name": "Hanoch",
        "age": 780,
        "occupation": {
            "name": "Our Teacher",
            "isSaint": True
        }
    },
    {
        "id": 6,
        "name": "Miryam",
        "age": 88,
        "occupation": {
            "name": "Prophet",
            "isSaint": True
        }
    }
]


def test_saints():
    response = client.get("/saints")
    assert response.status_code == 200


    assert response.json() ==saintsTrue






short=[
    [
        "Abraham",
        {
            "name": "Our Father",
            "isSaint": False
        }
    ],
    [
        "Sara",
        {
            "name": "Our Mother",
            "isSaint": True
        }
    ],
    [
        "Yakov",
        {
            "name": "Our 3rd Father",
            "isSaint": True
        }
    ],
    [
        "Hanoch",
        {
            "name": "Our Teacher",
            "isSaint": True
        }
    ],
    [
        "Metushelah",
        {
            "name": "Long Living",
            "isSaint": False
        }
    ],
    [
        "Miryam",
        {
            "name": "Prophet",
            "isSaint": True
        }
    ]
]
def test_short_desc():
    response = client.get("/short-desc")
    assert response.status_code == 200
    # with open('customer.json', 'r') as file:
    #     content = file.read()

    assert response.json() ==short




def test_whoname_existe():
    # Testing for a name that exists (Sara)
    response = client.get("/who?name=Sara")
    assert response.status_code == 200

    # Verify that the response body contains the expected data
    assert response.json() == {
        "id": 2,
        "name": "Sara",
        "age": 90,
        "occupation": {
            "name": "Our Mother",
            "isSaint": True
        }
    }




def test_whoname_not_existe():
    # Testing for a name that exists (Sara)
    response = client.get("/who?name=Sa")
    assert response.status_code == 200
    assert response.json() == "'No such customer'"


def test_saints_update():
    # Testing for a name that exists (Sara)
    response = client.get("/saintsup?isSaint=true")
    assert response.status_code == 200
    assert response.json() == [
    {
        "id": 2,
        "name": "Sara",
        "age": 90,
        "occupation": {
            "name": "Our Mother",
            "isSaint": True
        }
    },
    {
        "id": 3,
        "name": "Yakov",
        "age": 110,
        "occupation": {
            "name": "Our 3rd Father",
            "isSaint": True
        }
    },
    {
        "id": 4,
        "name": "Hanoch",
        "age": 780,
        "occupation": {
            "name": "Our Teacher",
            "isSaint": True
        }
    },
    {
        "id": 6,
        "name": "Miryam",
        "age": 88,
        "occupation": {
            "name": "Prophet",
            "isSaint": True
        }
    }
]



def test_saints_update_FALSE():
    # Testing for a name that exists (Sara)
    response = client.get("/saintsup?isSaint=false")
    assert response.status_code == 200
    assert response.json() == [
    {
        "id": 1,
        "name": "Abraham",
        "age": 120,
        "occupation": {
            "name": "Our Father",
            "isSaint": False
        }
    },
    {
        "id": 5,
        "name": "Metushelah",
        "age": 920,
        "occupation": {
            "name": "Long Living",
            "isSaint": False
        }
    }
]











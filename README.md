# Backend API Server - Capstone Project - First Hand Market API

# Name of the project: The FirstHand Market API

**Introduction. What is this API about:** For this project decided to create this First Hand Market RESFULL API that stores registers of persons who produce consumer goods for trade, and people who buys them for personal consumption or for commercial purposes and relate them by registering trades and sales and purchases according to the role of the user in the system.

## About stack
**Python 3.9.5**
**ProstgreSQL**

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment
We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies
Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:


```bash
pip install -r requirements.txt
```

## Running the server
From within the `./backend` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```
```bash
export FLASK_END=development;
```

To run the server, execute:

```bash
flask run --reload
```
# Set Postgresql Database
Set development and test databases
 createdb fhmarket && createdb fhmarket_test

# Populate databases
psql fhmarket < fhmarket_test.psql
psql fhmarket_test < fhmarket_test.psql

# Getting Started

API Resource: 
**Producer**
Aquella persona que cultiva o elabora un producto para su comercialización.
**Buyer**
Aquella persona que compra bienes de consumo para su uso o comercialización.
**Sale**
Negocio jurídico que surge de la confluencia de voluntad entre alguien que vende y otro que compra

### API endpoints EndPoints Testing
````
- GET /producers
Sample Request
    curl http://127.0.0.1:5000/producers?page=1
Sample Output
    {
    "data": [
        {
        "id": 1,
        "localization": "Upala",
        "name": "ariel",
        "products": "papaya"
        },
        {
        "id": 2,
        "localization": "Santana",
        "name": "Miguel",
        "products": "Cebolla"
        }
    ],
    "message": "Producers endpoint to retrieve all producers, GET Request"
    }
- POST /producers
Sample Request

    curl http://127.0.0.1:5000/producers -X POST -H "Content-Type:application/json" -d "{\"name\":\"Mauricio Cordoba\", \"country\":\"Guatemala\", \"products\":[\"Aguacate\",\"Lentejas\"]}"
Sample Output

- DELETE /producers/id
Sample CURL Request
    curl http://127.0.0.1:5000/producers/3 -X DELETE

- PATCH /producers/id
Sample CURL request
    curl http://127.0.0.1:5000/producers/1 -X PATCH -H "Content-Type:application/json" -d "{\"products\":\"menta\", \"name\":\"Ariel\", \"localization\":\"Puntarenas\"}"
````
## 2 · Buyer Resource 
````

- GET /buyers
    curl http://127.0.0.1:5000/buyers 

- POST /buyers
Request Sample
    curl http://127.0.0.1:5000/buyers -X POST -H "Content-Type:application/json" -d "{\"name\":\"Alvaro Saborio\",\"comercialized_products\":[\"miel\", \"tapa e dulce\", \"melcochas\", \"cajetas\"]}"

Sample Response
{
  "success": true,
  "the_new_buyer": {
    "comercialized_product": [
      "papaya",
      "sandia",
      "melon"
    ],
    "id": 1,
    "name": "Julio Mena"
  }
}

DELETE /buyers/<id>
Request Sample
    curl -X DELETE http://127.0.0.1:5000/buyers/1
Response Sample
{
  "data": {
    "comercialized_products": [
      "papaya",
      "sandia",
      "melon"
    ],
    "id": 2,
    "name": "Julio Mena"
  },
  "success": true
}

PATCH /buyers/<id>
Sample Request
    curl -X PATCH http://127.0.0.1:5000/buyers/3 -H "Content-Type:application/json" -d "{\"name\":\"Victor Evaristo\"}"

Sample Response
    {
        "data": {
            "comercialized_products": [
            "papaya",
            "sandia",
            "melon"
            ],
            "id": 3,
            "name": "Victor Evaristo"
        },
        "success": true
    }
````
## 3 - Sales Resource 
````

GET sales |Retrieves all sales on sales table.
Sample Request: 
    curl http://127.0.0.1:5000/sales

POST | Create a new SALE object record
    curl http://127.0.0.1:5000/sales -X POST -H "Content-Type:application/json" -d "{\"producer_id\":\"1\", \"buyer_id\":\"2\", \"sale_detail\":[{\"Product\":\"Pipa\",\"quantity\":\"200\"},{\"Product\":\"Papa\",\"quantity\":\"200 kilos\"}]}"

POST REQUEST SIN SALE DETAIL column
    curl http://127.0.0.1:5000/sales -X POST -H "Content-Type:application/json" -d "{\"producer_id\":\"1\", \"buyer_id\":\"2\"}"

GET /producers/<int:p_id>/sales | Sales by producers: Retrieves all the sales made by a producer
Sample Request
    curl  http://127.0.0.1:5000/producers/1/sales -H "Authorization: Bearer <THE_ROLE_ACCESS_TOKEN>"
    
    curl  http://127.0.0.1:5000/producers/1/sales -H "Authorization: Bearer <THE_ROLE_ACCESS_TOKEN>"

Sample Response

GET /buyers/<int_b_id>/sales | Purchases made by a buyer
Sample Request
curl http://127.0.0.1:5000/buyers/1/sales -H "Authorization: Bearer <ROLE_ACCESS_TOKEN>"

````
## FOR TESTING
````
To run the tests, run
    dropdb fhmarket_test && createdb fhmarket_test

    python test_flaskr.py
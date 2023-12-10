# API Code Task

## Contents

1. [Task Description](#task-description)
2. [Getting Started](#getting-started)
3. [My Solution](#my-solution)
4. [Future Improvements](#future-improvements)

## Task Description

- Create a REST API that allows an admin user to:
  - create a customer
  - create accounts for that customer
  - transfer money between accounts

## Getting Started

### Install dependencies

```
pip install -r requirements.txt
```

### Run server

```
python main.py  
```

### Run tests

```
pytest tests/test_api.py
```

### API documentation (Swagger)

```
http://127.0.0.1:8899/docs
```

## My Solution

- I decided to use FastApi as it provides API docs out the box
- I implemented the 3 main endpoints as per the requirements of the task and a few more
- The endpoints were designed keeping REST standards in mind
- Endpoint behaviours are tested using Api Functional tests
- SQLite was used for data storage

## Usage

- Add customers to the database by using POST `/api/v1/customers`
- You can view your customers by using GET `/api/v1/customers` or POST `api/v1/customers/{customer_id}`
- You can create accounts for customers but using POST `/api/v1/accounts/{customer_id}/accounts/`
- You can transfer money between accounts using POST `/api/v1/accounts/transfer`

## Future Improvements

- Logging can be improved to log to a specific service as well as introduction prefixes and log levels
- Tests can be improved by handling the test data in transactions instead of a test database
- Code inside certain endpoints can be abstracted out to maintain separation of concerns
- Authentication to protect endpoints (for example JWT)
- Proper hashing needs to be done to protect passwords
- Fix warnings in tests
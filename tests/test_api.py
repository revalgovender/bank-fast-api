import uuid

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

"""Tests for endpoint /v1/customers/

    All tests in this group test the behaviour of this endpoint
    """


def test_it_will_create_a_customer():
    # Arrange.
    email_suffix = str(uuid.uuid4())
    email = "testuser@" + email_suffix + ".com"
    client.post(
        "/api/v1/customers",
        json={"email": email, "password": "thisisatest"},
    )

    # Act.
    response = client.post(
        "/api/v1/customers",
        json={"email": email, "password": "thisisatest"},
    )

    # Assert.
    assert response.status_code == 409


def test_it_will_return_a_409_error_if_email_exists():
    # Arrange.
    email_suffix = str(uuid.uuid4())
    email = "testuser@" + email_suffix + ".com"
    response = client.post(
        "/api/v1/customers",
        json={"email": email, "password": "thisisatest"},
    )

    # Act.
    response = client.post(
        "/api/v1/customers",
        json={"email": email, "password": "thisisatest"},
    )
    retrieved_customer = response.json()

    # Assert.
    assert response.status_code == 409


"""Tests for endpoint /v1/customers/

    All tests in this group test the behaviour of this endpoint
    """


def test_it_will_retrieve_a_customer():
    # Arrange.
    email_suffix = str(uuid.uuid4())
    email = "testuser@" + email_suffix + ".com"
    response = client.post(
        "/api/v1/customers",
        json={"email": email, "password": "thisisatest"},
    )
    customer = response.json()

    # Act.
    response = client.get("/api/v1/customers/" + str(customer['id']))
    customer_retrieved = response.json()

    # Assert.
    assert response.status_code == 200
    assert customer_retrieved['email'] == email
    assert customer_retrieved['id'] == customer['id']
    assert customer_retrieved['accounts'] == []


def test_it_will_return_a_404_when_customer_cannot_be_found():
    # Arrange.
    bad_customer_id = '4948484'

    # Act.
    response = client.get("/api/v1/customers/" + bad_customer_id)

    # Assert.
    assert response.status_code == 404


"""Tests for endpoint /v1/customers/

    All tests in this group test the behaviour of this endpoint
    """

def test_it_will_return_all_customers():
    # Arrange.
    email_suffix = str(uuid.uuid4())
    email = "testuser@" + email_suffix + ".com"
    response = client.post(
        "/api/v1/customers",
        json={"email": email, "password": "thisisatest"},
    )
    customer = response.json()

    # Act.
    response = client.get("/api/v1/customers/")
    customers_retrieved = response.json()

    # Assert.
    assert response.status_code == 200
    assert type(customers_retrieved) == list


"""Tests for endpoint /customers/{customer_id}/accounts

    All tests in this group test the behaviour of this endpoint
    """


def test_it_will_create_a_bank_account_for_a_customer_with_initial_deposit():
    # Arrange.
    email_suffix = str(uuid.uuid4())
    email = "testuser@" + email_suffix + ".com"
    response = client.post(
        "/api/v1/customers",
        json={"email": email, "password": "thisisatest"},
    )
    customer = response.json()
    customer_id = str(customer['id'])

    # Act.
    response = client.post(
        "/api/v1/customers/" + customer_id + "/accounts/",
        json={"balance": 100},
    )
    account = response.json()

    # Assert.
    assert response.status_code == 200
    assert account['balance'] == 100


def test_it_will_return_a_404_if_customer_cannot_be_found():
    # Arrange.
    customer_id = str(7878)

    # Act.
    response = client.post(
        "/api/v1/customers/" + customer_id + "/accounts/",
        json={"balance": 100},
    )
    account = response.json()

    # Assert.
    assert response.status_code == 404


"""Tests for endpoint /accounts/{account_id}

    All tests in this group test the behaviour of this endpoint
    """


def test_it_will_retrieve_bank_account_by_account_id():
    # Arrange.
    email_suffix = str(uuid.uuid4())
    email = "testuser@" + email_suffix + ".com"
    response = client.post(
        "/api/v1/customers",
        json={"email": email, "password": "thisisatest"},
    )
    customer = response.json()
    customer_id = str(customer['id'])
    response = client.post(
        "/api/v1/customers/" + customer_id + "/accounts/",
        json={"balance": 100},
    )
    account_created = response.json()
    account_created_id = str(account_created['id'])

    # Action.
    response = client.get("/api/v1/accounts/" + account_created_id)
    account_retrieved = response.json()

    # Assert.
    assert response.status_code == 200
    assert account_retrieved['balance'] == 100


def test_it_will_return_a_404_error_if_account_does_not_exist():
    # Arrange.
    bad_account_id = str(789789)

    # Action.
    response = client.get("/api/v1/accounts/" + bad_account_id)
    account_retrieved = response.json()

    # Assert.
    assert response.status_code == 404


"""Tests for endpoint /accounts/transfer

    All tests in this group test the behaviour of this endpoint
    """


def test_it_will_transfer_money_from_one_account_to_another():
    # Arrange.
    customer_with_account_one = create_customer_with_account("dave", 100)
    customer_with_account_two = create_customer_with_account("mary", 50)
    body = {
        "source_account_id": customer_with_account_one['id'],
        "destination_account_id": customer_with_account_two['id'],
        "amount": 10
    }

    # Act.
    response = client.post("/api/v1/accounts/transfer", json=body)
    transfer_result = response.json()

    # Assert.
    assert response.status_code == 200
    assert transfer_result['source_account']['balance'] == 90
    assert transfer_result['destination_account']['balance'] == 60


def test_it_will_return_a_404_error_when_one_account_does_not_exist():
    # Arrange.
    customer_with_account_one = create_customer_with_account("dave", 100)
    bad_account_id = 1231321
    body = {
        "source_account_id": customer_with_account_one['id'],
        "destination_account_id": bad_account_id,
        "amount": 10
    }

    # Act.
    response = client.post("/api/v1/accounts/transfer", json=body)

    # Assert.
    assert response.status_code == 404


def test_it_will_return_a_422_error_when_one_there_is_insufficient_funds():
    # Arrange.
    customer_with_account_one = create_customer_with_account("dave", 50)
    customer_with_account_two = create_customer_with_account("mary", 100)
    body = {
        "source_account_id": customer_with_account_one['id'],
        "destination_account_id": customer_with_account_two['id'],
        "amount": 55
    }

    # Act.
    response = client.post("/api/v1/accounts/transfer", json=body)

    # Assert.
    assert response.status_code == 422


def test_it_will_return_a_400_error_when_account_id_are_identical():
    # Arrange.
    body = {
        "source_account_id": 1,
        "destination_account_id": 1,
        "amount": 55
    }

    # Act.
    response = client.post("/api/v1/accounts/transfer", json=body)

    # Assert.
    assert response.status_code == 400


"""Tests helpers
    """


def create_customer_with_account(email_prefix: str, balance: int):
    email_suffix = str(uuid.uuid4())
    email = email_prefix + "@" + email_suffix + ".com"
    response = client.post(
        "/api/v1/customers",
        json={"email": email, "password": "thisisatest"},
    )
    customer = response.json()
    customer_id = str(customer['id'])
    response = client.post(
        "/api/v1/customers/" + customer_id + "/accounts/",
        json={"balance": balance},
    )

    return response.json()

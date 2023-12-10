from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from bank.db import crud, models, schemas

from bank.db.database import SessionLocal, engine

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/v1/customers/", response_model=schemas.Customer)
def create(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    # Check if customer exists.
    try:
        db_customer = crud.get_customer_by_email(db, email=customer.email)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail="Something went wrong while retrieving customer.")

    if db_customer:
        raise HTTPException(status_code=409, detail="Email already registered")
    return crud.create_customer(db=db, customer=customer)


@router.get("/v1/customers/{customer_id}", response_model=schemas.Customer)
def show(customer_id: int, db: Session = Depends(get_db)):
    # Check if customer exists
    try:
        db_customer = crud.get_customer_by_id(db, customer_id=customer_id)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail="Something went wrong while retrieving customer.")

    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer cannot be found")
    return db_customer


@router.get("/v1/customers/", response_model=list[schemas.Customer])
def list_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        return crud.get_customers(db, skip=skip, limit=limit)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail="Something went wrong while retrieving customers.")


@router.post("/v1/customers/{customer_id}/accounts/", response_model=schemas.Account)
def create(customer_id: int, account: schemas.AccountCreate, db: Session = Depends(get_db)):
    # Check if customer exists
    try:
        db_customer = crud.get_customer_by_id(db, customer_id=customer_id)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail="Something went wrong while retrieving customer.")

    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer cannot be found.")

    try:
        return crud.create_customer_account(db=db, account=account, customer_id=customer_id)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail="Something went wrong while creating account.")


@router.get("/v1/accounts/{account_id}", response_model=schemas.Account)
def show(account_id: int, db: Session = Depends(get_db)):
    # Check if account exists
    try:
        db_account = crud.get_account_by_id(db, account_id=account_id)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail="Something went wrong while retrieving account.")

    if not db_account:
        raise HTTPException(status_code=404, detail="Account cannot be found.")
    return db_account


@router.post("/v1/accounts/transfer", response_model=schemas.AccountTransferResponse)
def transfer(transfer_data: schemas.AccountTransferRequest, db: Session = Depends(get_db)):
    # Check if both accounts are the same
    if transfer_data.source_account_id == transfer_data.destination_account_id:
        raise HTTPException(status_code=400, detail="Cannot transfer from the same account")

    # Check if both source and destination accounts exist
    source_account = db.query(models.Account).filter(models.Account.id == transfer_data.source_account_id).first()
    destination_account = db.query(models.Account).filter(
        models.Account.id == transfer_data.destination_account_id).first()
    if source_account is None or destination_account is None:
        print('reval')
        raise HTTPException(status_code=404, detail="One or both accounts do not exist")

    # Check if the source account has enough balance for the transfer
    if source_account.balance < transfer_data.amount:
        raise HTTPException(status_code=422, detail="Insufficient balance for the transfer")

    # Update the balances for both accounts
    source_account.balance -= transfer_data.amount
    destination_account.balance += transfer_data.amount
    db.commit()

    return {
        "source_account": {
            "balance": source_account.balance
        },
        "destination_account": {
            "balance": destination_account.balance
        }
    }

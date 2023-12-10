from sqlalchemy.orm import Session

from . import models, schemas


def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()


def get_customer_by_email(db: Session, email: str):
    return db.query(models.Customer).filter(models.Customer.email == email).first()


def get_customer_by_id(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()


def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).offset(skip).limit(limit).all()


def create_customer(db: Session, customer: schemas.CustomerCreate):
    fake_hashed_password = customer.password + "notreallyhashed"
    db_customer = models.Customer(email=customer.email, hashed_password=fake_hashed_password)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def get_accounts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Account).offset(skip).limit(limit).all()


def get_account_by_id(db: Session, account_id: int):
    return db.query(models.Account).filter(models.Account.id == account_id).first()


def create_customer_account(db: Session, account: schemas.AccountCreate, customer_id: int):
    db_account = models.Account(**account.dict(), customer_id=customer_id)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

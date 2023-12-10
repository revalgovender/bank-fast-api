from pydantic import BaseModel


class AccountBase(BaseModel):
    balance: int


class AccountCreate(AccountBase):
    pass


class Account(AccountBase):
    id: int
    customer_id: int

    class Config:
        from_attributes = True


class AccountTransferRequest(BaseModel):
    source_account_id: int
    destination_account_id: int
    amount: int


class AccountTransferResponse(BaseModel):
    source_account: AccountBase
    destination_account: AccountBase


class CustomerBase(BaseModel):
    email: str


class CustomerCreate(CustomerBase):
    password: str


class Customer(CustomerBase):
    id: int
    is_active: bool
    accounts: list[Account] = []

    class Config:
        from_attributes = True

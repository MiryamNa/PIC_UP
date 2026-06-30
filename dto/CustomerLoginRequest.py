from pydantic import BaseModel


class CustomerLoginRequest(BaseModel):
    firstName: str
    password: str
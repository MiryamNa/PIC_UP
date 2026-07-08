from dto.CustomerLoginRequest import CustomerLoginRequest
from repository.customer_repository import CustomerRepository
from dto.customerDTO import CustomerDTO
from models.customer import Customer
from fastapi import HTTPException

class CustomerService:
    def __init__(self):
        self.repo = CustomerRepository()

    async def create(self, data:CustomerDTO ):
        customer = Customer(
            clientId=data.clientId,
            firstName=data.firstName,
            lastName=data.lastName,
            email=data.email,
            phone=data.phone,
            password=data.password
        )
        return await self.repo.create(customer)

    async def login(self, payload: CustomerLoginRequest):
        customer = await Customer.find_one(
            {
                "firstName": payload.firstName,
                "password": payload.password
            }
        )
        if not customer:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return customer

    async def list_all(self):
        return await self.repo.get_all()

    async def get_by_id(self, customer_id: str):
        return await self.repo.get(customer_id)

    async def update(self, customer_id: str, data: Customer):
        data = data.dict()
        return await self.repo.update(customer_id, data)

    async def remove(self, customer_id: str):
        return await self.repo.delete(customer_id)
from models.customer import Customer
from dto.CustomerDTO import CustomerDTO

class CustomerRepository:
    async def create(self, data: Customer):
        customer = data
        await customer.insert()
        return customer

    async def get(self, customer_id: int):
        return await Customer.find_one(Customer.clientId == customer_id)

    async def get_all(self):
        return await Customer.find_all().to_list()

    async def update(self, customer_id: int, data: dict):
        customer = await Customer.find_one(Customer.clientId == customer_id)
        if customer:
            await customer.update({"$set": data})
            return customer
        return None

    async def delete(self, customer_id: int):
        customer = await Customer.find_one(Customer.clientId == customer_id)
        if customer:
            await customer.delete()
            return True
        return False
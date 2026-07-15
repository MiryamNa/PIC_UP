from fastapi import APIRouter, HTTPException
from dto.customerDTO import CustomerDTO
from services.customer_service import CustomerService
from dto.CustomerLoginRequest import CustomerLoginRequest
router = APIRouter(prefix="/customer", tags=["Customers"])
service = CustomerService()

@router.post("/")
async def create_customer(data: CustomerDTO):
    return await service.create(data)

@router.post("/login")
async def login_customer(payload: CustomerLoginRequest):
    return await service.login(payload)
    
@router.get("/")
async def get_customers():
    return await service.list_all()

@router.get("/{customer_id}")
async def get_customer(customer_id: str):
    customer = await service.get_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.put("/{customer_id}")
async def update_customer(customer_id: str, data:CustomerDTO):
    customer = await service.update(customer_id, data)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.delete("/{customer_id}")
async def delete_customer(customer_id: str):
    success = await service.remove(customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted"}
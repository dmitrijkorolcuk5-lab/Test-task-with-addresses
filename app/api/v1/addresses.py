from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.schemas.address import AddressCreate, AddressOut
from arq.connections import ArqRedis
from app.services.address_service import AddressService

router = APIRouter()

# Dependency to get the Redis pool from the application state
def get_redis(request: Request) -> ArqRedis | None:
    return getattr(request.app.state, "redis_pool", None)

# Dependency to create an instance of the AddressService
def get_address_service(db: AsyncSession = Depends(get_db), redis: ArqRedis | None = Depends(get_redis)) -> AddressService:
    return AddressService(db, redis)

@router.post("/", response_model=AddressOut, status_code=status.HTTP_201_CREATED)
async def create_address(address_data: AddressCreate, service: AddressService = Depends(get_address_service)):
    new_address = await service.create_address_and_enqueue_validation(address_data)
    return new_address

@router.get("/", response_model=List[AddressOut])
async def get_addresses(skip: int = 0, limit: int = 100, service: AddressService = Depends(get_address_service)):
    return await service.get_all_addresses(skip=skip, limit=limit)

@router.get("/{address_id}", response_model=AddressOut)
async def get_address(address_id: int, service: AddressService = Depends(get_address_service)):
    address = await service.get_address_by_id(address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(address_id: int, service: AddressService = Depends(get_address_service)):
    deleted = await service.delete_address_by_id(address_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Address not found")
    return None
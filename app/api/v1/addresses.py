from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.models.address import Address
from app.schemas.address import AddressCreate, AddressOut
from sqlalchemy.future import select
from arq import create_pool
from arq.connections import RedisSettings

router = APIRouter()

@router.post("/", response_model=AddressOut, status_code=status.HTTP_201_CREATED)
async def create_address(address_data: AddressCreate, db: AsyncSession = Depends(get_db)):
    new_address = Address(**address_data.model_dump())
    db.add(new_address)
    await db.commit()
    await db.refresh(new_address)
    
    redis = await create_pool(RedisSettings(host='localhost', port=6380))
    await redis.enqueue_job('validate_address_task', new_address.id)
    
    return new_address

@router.get("/", response_model=List[AddressOut])
async def get_addresses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Address))
    return result.scalars().all()

@router.get("/{address_id}", response_model=AddressOut)
async def get_address(address_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Address).where(Address.id == address_id))
    address = result.scalar_one_or_none()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(address_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Address).where(Address.id == address_id))
    address = result.scalar_one_or_none()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    await db.delete(address)
    await db.commit()
    return None
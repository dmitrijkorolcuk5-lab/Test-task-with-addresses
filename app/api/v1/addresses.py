from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.address import AddressCreate, AddressRead
from app.services.address_service import AddressService

router = APIRouter()

@router.post("/", response_model=AddressRead)
async def create_new_address(
    address_in: AddressCreate, 
    db: AsyncSession = Depends(get_db)
):
    
    service = AddressService(db)
    try:
        
        new_address = await service.create_and_validate(address_in.model_dump())
        return new_address
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.address import AddressRepository
from app.services.external_api import ShipEngineClient
class AddressService:
    def __init__(self, db: AsyncSession):
        self.repository = AddressRepository(db)
        self.client = ShipEngineClient()
    
    async def create_and_validate(self, address_in_data: dict):
        is_valid = await self.client.validate_address(address_in_data)
        address_in_data["is_valid"] = is_valid
        return await self.repository.create(address_in_data)
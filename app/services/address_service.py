from sqlalchemy.ext.asyncio import AsyncSession
from arq.connections import ArqRedis
from app.repositories.address import AddressRepository
from app.schemas.address import AddressCreate
from app.models.address import Address
from typing import List

class AddressService:
    def __init__(self, db_session: AsyncSession, redis_pool: ArqRedis = None):
        self.repo = AddressRepository(db_session)
        self.redis = redis_pool

    async def get_all_addresses(self, skip: int = 0, limit: int = 100) -> List[Address]:
        return await self.repo.get_all(skip=skip, limit=limit)

    # НОВИЙ МЕТОД: Отримує загальну кількість через репозиторій
    async def get_addresses_count(self) -> int:
        return await self.repo.get_count()

    async def get_address_by_id(self, address_id: int) -> Address | None:
        return await self.repo.get_by_id(address_id)

    async def create_address_and_enqueue_validation(self, address_data: AddressCreate) -> Address:
        new_address = await self.repo.create(address_data.model_dump())
        await self.repo.session.commit()
        await self.repo.session.refresh(new_address)

        if self.redis:
            await self.redis.enqueue_job('validate_address_task', new_address.id)
        return new_address

    async def delete_address_by_id(self, address_id: int) -> bool:
        deleted = await self.repo.delete(address_id)
        if deleted:
            await self.repo.session.commit()
        return deleted
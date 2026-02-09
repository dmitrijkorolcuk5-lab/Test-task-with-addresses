from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class AddressBase(BaseModel):
    name: str = Field(description="Recipient's full name", example="Dmytro Shevchenko")
    phone: Optional[str] = Field(None, description="Contact phone number", example="+380501234567")
    address_line1: str = Field( description="Street address and house number", example="1600 Pennsylvania Avenue NW")
    address_line2: Optional[str] = Field(None, description="Apartment, suite, etc.")
    city_locality: str = Field( description="City or locality", example="Washington")
    state_province: str = Field(..., description="State or province", example="DC")
    postal_code: str = Field(..., description="Postal code", example="20500")
    country_code: str = Field(..., description="ISO 3166-1 alpha-2 country code", example="US")

class AddressCreate(AddressBase):
    pass


class AddressOut(AddressBase):
    id: int
    is_valid: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
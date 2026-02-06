from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class AddressBase(BaseModel):
    name: str = Field(..., description="Recipient's full name", example="Dmytro Shevchenko")
    phone: Optional[str] = Field(None, description="Contact phone number", example="+380501234567")
    address_line1: str = Field(..., description="Street address and house number", example="1 Khreshchatyk St")
    address_line2: Optional[str] = Field(None, description="Apartment, suite, etc.")
    city_locality: str = Field(..., description="City or locality", example="Kyiv")
    state_province: str = Field(..., description="State or province", example="Kyiv Region")
    postal_code: str = Field(..., description="Postal code", example="01001")
    country_code: str = Field(..., description="ISO 3166-1 alpha-2 country code", example="UA")


class AddressCreate(AddressBase):
    pass


class AddressRead(AddressBase):
    id: int
    is_valid: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
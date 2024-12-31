import re
from datetime import datetime

from pydantic import BaseModel, model_validator, Field, EmailStr, field_validator


class UserRegistration(BaseModel):
    first_name: str = Field(..., min_length=2,
                            description="Лише літери, мінімум 2 символи")
    last_name: str = Field(..., min_length=2,
                           description="Лише літери, мінімум 2 символи")
    email: EmailStr
    password: str = Field(..., min_length=8,
                          description="Мінімум 8 символів, включає велику, маленьку літеру, цифру і спеціальний символ")
    phone: str = Field(...,  description="Міжнародний формат, 10-15 цифр")

    create_date: datetime = Field(datetime.now())

    @field_validator('first_name')
    def validate_first_name(cls, value):
        if not re.match(r'^[A-Za-zА-Яа-я]+$', value):
            raise ValueError("Поле має містити лише літери")
        return value

    @field_validator('last_name')
    def validate_last_name(cls, value):
        if not re.match(r'^[A-Za-zА-Яа-я]+$', value):
            raise ValueError("Поле має містити лише літери")
        return value

    @field_validator("password")
    def validate_password(cls, value):
        if not re.search(r'[A-Z]', value):
            raise ValueError("Пароль повинен містити хоча б одну велику літеру")
        if not re.search(r'[a-z]', value):
            raise ValueError("Пароль повинен містити хоча б одну маленьку літеру")
        if not re.search(r'\d', value):
            raise ValueError("Пароль повинен містити хоча б одну цифру")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValueError("Пароль повинен містити хоча б один спеціальний символ")
        return value

    @field_validator("phone")
    def validate_phone(cls, value):
        if not re.match(r'^\+?\d{10,15}$', value):
            raise ValueError("Телефон повинен бути у міжнародному форматі, 10-15 цифр")
        return value

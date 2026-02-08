from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: Optional[int] = None
    cedula: str
    nombre_completo: str
    email: EmailStr
    telefono: Optional[str] = None
    genero: Optional[str] = None
    password_hash: str
    id_rol: int

class BiotypeUpdate(BaseModel):
    biotipo: str
    confianza_ia: float

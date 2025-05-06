from sqlmodel import SQLModel
from data.models import EstadoUsuario

class UsuarioCreate(SQLModel):
    nombre: str
    email: str
    estado: EstadoUsuario
    premium: bool = False
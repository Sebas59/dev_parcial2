from sqlmodel import SQLModel
from data.models import *
from datetime import datetime

class UsuarioCreate(SQLModel):
    nombre: str
    email: str
    estado: EstadoUsuario
    premium: bool = False

class TareaCreate(SQLModel):
    nombre: str
    descripcion: str
    estado: EstadoTarea
    Usuario_id: int

class TareaRead(SQLModel):
    id: int
    nombre: str
    descripcion: str
    fecha_creacion: datetime
    fecha_modificacion: datetime
    estado: EstadoTarea
    Usuario_id: int
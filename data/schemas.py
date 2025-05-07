from sqlmodel import SQLModel
from data.models import *
from datetime import datetime

class UsuarioCreate(SQLModel):
    nombre: str
    email: str
    estado: EstadoUsuario
    premium: bool 

class TareaCreate(SQLModel):
    nombre: str
    descripcion: Optional[str]= None
    estado: Optional[EstadoTarea] = EstadoTarea.pendiente
    usuario_id: int

class TareaRead(SQLModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    fecha_creacion: datetime
    fecha_modificacion: datetime
    estado: EstadoTarea
    usuario_id: int
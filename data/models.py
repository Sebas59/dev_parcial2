from sqlmodel import SQLModel, Field,Relationship
from typing import Optional
import enum

class EstadoUsuario(str, enum.Enum):
    activo = "activo"
    inactivo = "inactivo"
    suspendido = "suspendido"

class EstadoTarea(str, enum.Enum):
    pendiente = "pendiente"
    en_ejecucion = "en_ejecucion"
    realizada = "realizada"
    cancelada = "cancelada"

class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    email: str
    estado: EstadoUsuario 
    premium: bool = Field(default=False)
    tareas: Optional["Tarea"] = Relationship(back_populates="usuario")

class Tarea(SQLModel, table=True):
    __tablename__ = "tareas"
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    estado: EstadoTarea
    usuario_id: int = Field(foreign_key="usuarios.id",nullable=False)
    usuario: Optional[Usuario]= Relationship(back_populates="tareas")
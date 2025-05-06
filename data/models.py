from sqlmodel import SQLModel, Field
import enum

class EstadoUsuario(str, enum.Enum):
    activo = "activo"
    inactivo = "inactivo"
    suspendido = "suspendido"

class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"
    id: int = Field(default=None, primary_key=True)
    nombre: str
    email: str
    estado: EstadoUsuario 
    premium: bool = Field(default=False)
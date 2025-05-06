from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy import and_
from fastapi import HTTPException, status
from typing import List
from data.models import Usuario, EstadoUsuario
from data.schemas import UsuarioCreate

async def create_user(usuario: UsuarioCreate, session: AsyncSession) -> Usuario:
    nuevo_usuario = Usuario(**usuario.dict())
    session.add(nuevo_usuario)
    try:
        await session.commit()
        await session.refresh(nuevo_usuario)
        return nuevo_usuario
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=400,
            detail="El nombre de usuario ya existe."
        )
    
async def obtener_usuarios(session: AsyncSession) -> List[Usuario]:
    result = await session.execute(select(Usuario))
    return result.scalars().all()

async def obtener_usuario_por_email(usuario_email: str, session: AsyncSession) -> Usuario:
    result = await session.execute(select(Usuario).where(Usuario.email == usuario_email))
    usuario = result.scalars().first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email del usuario no encontrado."
        )
    return usuario

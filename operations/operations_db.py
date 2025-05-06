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

async def actualizar_usuario(usuario_email: str, usuario: UsuarioCreate, session: AsyncSession) -> Usuario:
    usuario_db = await obtener_usuario_por_email(usuario_email, session)
    if usuario.email != usuario_db.email:
        result = await session.execute(
            select(Usuario).where(Usuario.email == usuario.email)
        )
        usuario_existente = result.scalars().first()
        if usuario_existente:
            raise HTTPException(status_code=400, detail="El nuevo email ya está en uso.")
    for key, value in usuario.dict().items():
        setattr(usuario_db, key, value)
    session.add(usuario_db)
    await session.commit()
    await session.refresh(usuario_db)
    return usuario_db

async def actualizar_usuario_premium(usuario_email:str, usuario_premium:bool, session:AsyncSession):
    usuario= await obtener_usuario_por_email(usuario_email, session)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    
    if usuario.premium != usuario_premium:
        usuario.premium = usuario_premium
        session.add(usuario)

    try:
        await session.commit()
        await session.refresh(usuario)
        return usuario 
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Error al actualizar el estado del usuario a premium.")
    
async def obtener_usuarios_inactivos_db(session:AsyncSession) -> List[Usuario]:
    result = await session.execute(
        select(Usuario).where(
             Usuario.estado == EstadoUsuario.inactivo, 
        )
    )
    return result.scalars().all()
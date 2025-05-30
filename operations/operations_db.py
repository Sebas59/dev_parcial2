from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy import and_
from fastapi import HTTPException, status
from typing import List
from datetime import datetime
from data.models import Usuario, Tarea, EstadoUsuario, EstadoTarea
from data.schemas import UsuarioCreate, TareaCreate, TareaRead

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
    
async def obtener_usuarios_db(session: AsyncSession) -> List[Usuario]:
    result = await session.execute(select(Usuario))
    return result.scalars().all()

async def obtener_usuario_por_email_db(usuario_email: str, session: AsyncSession) -> Usuario:
    result = await session.execute(select(Usuario).where(Usuario.email == usuario_email))
    usuario = result.scalars().first()
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Email del usuario no encontrado."
        )
    return usuario

async def actualizar_estado_usuario_db(email: str, estado: EstadoUsuario, session: AsyncSession):
    usuario = await obtener_usuario_por_email_db(email, session)
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.estado = estado
    session.add(usuario)
    
    try:
        await session.commit()
        return usuario
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Error al actualizar el estado")
    
async def actualizar_usuario_premium_db(usuario_email:str, usuario_premium:bool, session:AsyncSession):
    usuario= await obtener_usuario_por_email_db(usuario_email, session)
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
    


async def obtener_usuarios_inactivos_premuim_db(session:AsyncSession):
    result = await session.execute(
        select(Usuario).where(
             Usuario.estado == EstadoUsuario.inactivo,
                Usuario.premium == True
        )
    )
    return result.scalars().all()
async def obtener_usuarios_inactivos_db(session:AsyncSession):
    query = select(Usuario).where(
        and_(
            Usuario.estado == EstadoUsuario.inactivo
        )
    )
    result = await session.execute(query)
    return result.scalars().all()

async def crear_tarea_db(tarea: TareaCreate, session: AsyncSession) -> Tarea:
    nueva_tarea = Tarea(**tarea.dict())
    session.add(nueva_tarea)
    await session.commit()
    await session.refresh(nueva_tarea)
    return nueva_tarea


async def obtener_tareas_db(session:AsyncSession)-> List[Tarea]:
    result = await session.execute(select(Tarea))
    return result.scalars().all()

async def obtener_tarea_por_usuario_db(usuario_id:int, session:AsyncSession)-> List[Tarea]:
    result = await session.execute(
        select(Tarea).where(Tarea.usuario_id== usuario_id)
    )
    return result.scalars().all()
    
async def actualizar_estado_tarea_db(tarea_id: int, nuevo_estado: str, session: AsyncSession) -> Tarea:
    result = await session.execute(select(Tarea).where(Tarea.id == tarea_id))
    tarea = result.scalar_one_or_none()
    if not tarea:
        raise ValueError("Tarea no encontrada")

    tarea.estado = nuevo_estado
    tarea.fecha_modificacion = datetime.utcnow()
    session.add(tarea)
    await session.commit()
    await session.refresh(tarea)
    return tarea

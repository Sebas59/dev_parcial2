from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from utils.connection_db import init_db
from utils.connection_db import init_db, get_session
from data.models import Usuario, EstadoUsuario
from data.schemas import UsuarioCreate

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from typing import List
from operations.operations_db import *

@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_db()
    yield
app = FastAPI(lifespan=lifespan)


@app.post("/usuarios/", response_model=Usuario, status_code=status.HTTP_201_CREATED, tags=["Usuarios"])
async def crear_usuario(usuario: UsuarioCreate, session: AsyncSession = Depends(get_session)):
    return await create_user(usuario, session)

@app.get("/usuarios/", response_model=List[Usuario], tags=["Usuarios"])
async def obtener_usuarios(session: AsyncSession = Depends(get_session)):
    return await obtener_usuarios_db(session)

@app.get("/usuarios/{usuario_email}", response_model=Usuario, tags=["Usuarios"])
async def obtener_usuario_por_email(usuario_email:str, session:AsyncSession=Depends(get_session)):
    return await obtener_usuario_por_email_db(usuario_email, session)

@app.patch("/usuarios/{email}/estado", response_model=Usuario, tags=["Usuarios"])
async def actualizar_estado_usuario(email: str, estado: EstadoUsuario, session: AsyncSession = Depends(get_session)):
    return await actualizar_estado_usuario_db(email, estado, session)

@app.patch("/usuarios/{usuario_email}/premium", response_model=Usuario, tags=["Usuarios"])
async def actualizar_usuario_premium(usuario_email:str, usuario_premium:bool, session:AsyncSession=Depends(get_session)):
    return await actualizar_usuario_premium_db(usuario_email, usuario_premium, session)

@app.get("/usuarios/Premium/inactivos",response_model=List[Usuario], tags=["Usuarios"])
async def obtener_usuarios_premium_inactivos_prem(session:AsyncSession=Depends(get_session)):
    usuario_premium_inactivo = await obtener_usuarios_inactivos_premuim_db(session)
    if not usuario_premium_inactivo:
        raise HTTPException(status_code=404, detail="No hay usuarios premium inactivos.")
    return usuario_premium_inactivo

@app.get("/usuarios/inactivos", response_model=List[Usuario], tags=["Usuarios"])
async def listar_usuarios_inactivos(session: AsyncSession = Depends(get_session)):
    usuarios = await obtener_usuarios_inactivos_db(session)
    if not usuarios:
        raise HTTPException(status_code=404, detail="No hay usuarios inactivos.")
    return usuarios


@app.post("/tareas", response_model=TareaRead, tags=["Tareas"])
async def crear_tarea(tarea: TareaCreate, session: AsyncSession = Depends(get_session)):
    return await crear_tarea_db(tarea, session)

@app.get("/tareas/", response_model=List[TareaRead], tags=["Tareas"])
async def obtener_tareas(session: AsyncSession = Depends(get_session)):
    return await obtener_tareas_db(session)

@app.get("/tareas/usuarios/{usuario_id}", response_model=List[TareaRead], tags=["Tareas"])
async def obtener_tareas_por_usuario(usuario_id: int, session: AsyncSession = Depends(get_session)):
    return await obtener_tarea_por_usuario_db(usuario_id, session)

@app.patch("/tareas/{tarea_id}/estado", response_model=TareaRead, tags=["Tareas"])
async def actualizar_estado_tarea(tarea_id: int, estado: EstadoTarea, session: AsyncSession = Depends(get_session)):
    try:
        return await actualizar_estado_tarea_db(tarea_id, estado, session)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
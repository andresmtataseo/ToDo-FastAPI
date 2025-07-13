from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routes.task import router as tasks_router
from routes.user import router as users_router
from routes.tag import router as tags_router

# Crear tablas en base a los modelos de forma automatica
Base.metadata.create_all(engine)

# Variable que contendra nuestra aplicacion de FastAPI
app = FastAPI()

# Informacion para nuestra aplicacion
app.title = 'ToDo API'
app.description = 'REST API for ToDo App with Tags System'
app.version = '1.0.0'

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas de nuestra app
app.include_router(tasks_router)
app.include_router(users_router)
app.include_router(tags_router)

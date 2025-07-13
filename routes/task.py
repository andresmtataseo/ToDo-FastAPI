from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
from models.task import Task
from models.tag import Tag
from schemas.task import TaskRead, TaskCreate, TaskUpdate
from utils.jwt import check_jwt
from typing import Optional, List

router = APIRouter(tags=['Tareas'])

@router.get('/tasks', dependencies=[Depends(check_jwt)])
def get_tasks(
    tags: Optional[str] = Query(None, description="Filtrar por etiquetas (separadas por coma)"),
    db: Session = Depends(get_db)
) -> list[TaskRead]:
    """Obtener tareas con filtrado opcional por etiquetas"""
    query = db.query(Task).filter(Task.is_active == 1)
    
    if tags:
        # Convertir string de tags a lista
        tag_names = [tag.strip() for tag in tags.split(',') if tag.strip()]
        
        if tag_names:
            # Filtrar tareas que tengan al menos una de las etiquetas especificadas
            query = query.join(Task.tags).filter(Tag.name.in_(tag_names))
    
    tasks = query.all()
    # Crear respuestas con conteo de etiquetas
    task_responses = []
    for task in tasks:
        task_data = TaskRead.from_orm(task)
        task_data.tag_count = len(task.tags)
        task_responses.append(task_data)
    
    return task_responses


@router.post('/tasks/create')
def create_task(task: TaskCreate, db: Session = Depends(get_db), task_payload: dict = Depends(check_jwt)) -> TaskRead:
    """Crear una nueva tarea con etiquetas obligatorias"""
    # Validar que haya al menos una etiqueta
    if not task.tag_names or len(task.tag_names) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'message': 'Debe proporcionar al menos una etiqueta para la tarea'}
        )
    
    new_task = Task(
        user_id=task_payload['id'],
        title=task.title,
        description=task.description,
        status=task.status.value,
    )

    # Asociar etiquetas (ahora obligatorias)
    for tag_name in task.tag_names:
        # Buscar la etiqueta existente o crear una nueva
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.add(tag)
            db.flush()  # Para obtener el ID de la nueva etiqueta
        
        new_task.tags.append(tag)

    # Registrar nueva tarea en base de datos
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    # Crear respuesta con conteo de etiquetas
    task_response = TaskRead.from_orm(new_task)
    task_response.tag_count = len(new_task.tags)
    
    return task_response


@router.put('/tasks/update/{id}', dependencies=[Depends(check_jwt)])
def update_task(id: int, task: TaskUpdate, db: Session = Depends(get_db)) -> dict[str, str]:
    """Actualizar una tarea existente con etiquetas obligatorias"""
    # Verificar si la tarea existe
    task_exist = db.query(Task).filter(Task.id == id).first()

    if not task_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'message': 'Tarea no encontrada'}
        )
    
    # Validar que haya al menos una etiqueta
    if not task.tag_names or len(task.tag_names) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'message': 'Debe proporcionar al menos una etiqueta para la tarea'}
        )
    
    # Actualizar campos básicos de la tarea
    db.query(Task).filter(Task.id == id).update({
        Task.title: task.title,
        Task.description: task.description,
        Task.status: task.status,
    })
    
    # Actualizar etiquetas (ahora obligatorias)
    # Limpiar etiquetas existentes
    task_exist.tags.clear()
    
    # Agregar nuevas etiquetas
    for tag_name in task.tag_names:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.add(tag)
            db.flush()
        
        task_exist.tags.append(tag)
    
    db.commit()

    return {
        'message': f'Tarea {task.title} actualizada con éxito'
    }


@router.delete('/tasks/delete/{id}', dependencies=[Depends(check_jwt)])
def delete_task(id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    """Eliminar una tarea (marcar como inactiva)"""
    task_exist = db.query(Task).filter(Task.id == id).first()

    if not task_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'message': 'Tarea no encontrada'}
        )
    
    # Marcar tarea como inactiva
    db.query(Task).filter(Task.id == id).update({
        Task.is_active: 0,
    })
    
    db.commit()

    return {
        'message': f'Tarea {task_exist.title} eliminada con éxito'
    }


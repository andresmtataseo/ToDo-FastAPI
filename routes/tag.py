from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.tag import Tag
from schemas.tag import TagRead, TagCreate, TagUpdate, TagWithTasks
from utils.jwt import check_jwt

router = APIRouter(tags=['Etiquetas'])


@router.get('/tags', dependencies=[Depends(check_jwt)])
def get_tags(db: Session = Depends(get_db)) -> list[TagRead]:
    tags = db.query(Tag).all()
    return [TagRead.from_orm(tag) for tag in tags]


@router.get('/tags/{tag_id}', dependencies=[Depends(check_jwt)])
def get_tag(tag_id: int, db: Session = Depends(get_db)) -> TagWithTasks:
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'message': 'Etiqueta no encontrada'}
        )
    
    # Crear respuesta con conteo de tareas
    tag_data = TagWithTasks.from_orm(tag)
    tag_data.task_count = len(tag.tasks)
    
    return tag_data


@router.post('/tags/create', dependencies=[Depends(check_jwt)])
def create_tag(tag: TagCreate, db: Session = Depends(get_db)) -> TagRead:
    # Verificar si la etiqueta ya existe
    existing_tag = db.query(Tag).filter(Tag.name == tag.name).first()
    
    if existing_tag:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'message': f'La etiqueta "{tag.name}" ya existe'}
        )
    
    new_tag = Tag(name=tag.name)
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    
    return TagRead.from_orm(new_tag)


@router.put('/tags/update/{tag_id}', dependencies=[Depends(check_jwt)])
def update_tag(tag_id: int, tag: TagUpdate, db: Session = Depends(get_db)) -> dict[str, str]:
    # Verificar si la etiqueta existe
    existing_tag = db.query(Tag).filter(Tag.id == tag_id).first()
    
    if not existing_tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'message': 'Etiqueta no encontrada'}
        )
    
    # Verificar si el nuevo nombre ya existe en otra etiqueta
    name_exists = db.query(Tag).filter(Tag.name == tag.name, Tag.id != tag_id).first()
    
    if name_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'message': f'La etiqueta "{tag.name}" ya existe'}
        )
    
    # Actualizar la etiqueta
    db.query(Tag).filter(Tag.id == tag_id).update({'name': tag.name})
    db.commit()
    
    return {
        'message': f'Etiqueta "{tag.name}" actualizada con éxito'
    }


@router.delete('/tags/delete/{tag_id}', dependencies=[Depends(check_jwt)])
def delete_tag(tag_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'message': 'Etiqueta no encontrada'}
        )
    
    # Verificar si la etiqueta está asociada a alguna tarea
    if tag.tasks:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'message': f'No se puede eliminar la etiqueta "{tag.name}" porque está asociada a {len(tag.tasks)} tarea(s)'}
        )
    
    # Eliminar la etiqueta
    db.delete(tag)
    db.commit()
    
    return {
        'message': f'Etiqueta "{tag.name}" eliminada con éxito'
    } 
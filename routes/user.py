from fastapi import APIRouter, Depends, HTTPException, status
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user import UserCreate, UserLogin
from utils.jwt import encode_jwt

router = APIRouter(tags=['Usuarios'])


@router.post('/users/create')
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_exist = db.query(User).filter(User.email == user.email).first()

    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={ 'message': 'El correo ya existe' }
        )

    bytes_password = user.password.encode()

    salt = gensalt()

    # Generamos la contrasena encriptada | el decode es para pasarlo de bytes a texto
    hashed_password = hashpw(bytes_password, salt).decode()

    # Registrar nuevo usuario en base de datos
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        'message': f'Usuario {user.email} creado con exito'
    }


@router.post('/users/login')
def login(user: UserLogin, db: Session = Depends(get_db)):
    user_exist = db.query(User).filter(User.email == user.email).first()

    # Si el usuario no existe no puede iniciar sesion
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={ 'message': 'El usuario no existe' }
        )
    
    # Pasamos la contrasena de texto a bytes
    password_bytes = user.password.encode()
    
    # Comparamos la contrasena que viene del front con la que tenemos en base de datos
    if checkpw(password_bytes, user_exist.password.encode()) == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={ 'message': 'Contrasena incorrecta' }
        )
    
    # Crear JWT
    token = encode_jwt({
        'id': user_exist.id,
        'email': user_exist.email,
    })
    
    return {
        'message': f'Bienvenido {user_exist.name}',
        'token': token,
    }
    
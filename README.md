# Sistema de Etiquetas (Tags) - ToDo API

## Descripción

Se ha implementado exitosamente un sistema completo de etiquetas para la ToDo API que permite:

- **Crear, leer, actualizar y eliminar etiquetas**
- **Asociar múltiples etiquetas a las tareas**
- **Filtrar tareas por etiquetas**
- **Crear etiquetas automáticamente al crear tareas**

## Estructura de la Base de Datos

### Tabla `tags`
- `id` (Primary Key)
- `name` (VARCHAR(50), UNIQUE)
- `created_at` (TIMESTAMP)

### Tabla `task_tags` (Relación muchos a muchos)
- `task_id` (Foreign Key → tasks.id)
- `tag_id` (Foreign Key → tags.id)
- Primary Key compuesta: (`task_id`, `tag_id`)

## Endpoints de Etiquetas

### 1. Obtener todas las etiquetas
```
GET /tags
Authorization: Bearer <token>
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "name": "urgente",
    "created_at": "2025-07-12T20:00:00"
  }
]
```

### 2. Obtener una etiqueta específica con sus tareas
```
GET /tags/{tag_id}
Authorization: Bearer <token>
```

### 3. Crear una nueva etiqueta
```
POST /tags/create
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "trabajo"
}
```

### 4. Actualizar una etiqueta
```
PUT /tags/update/{tag_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "trabajo-urgente"
}
```

### 5. Eliminar una etiqueta
```
DELETE /tags/delete/{tag_id}
Authorization: Bearer <token>
```

**Nota:** Solo se puede eliminar una etiqueta si no está asociada a ninguna tarea.

## Endpoints de Tareas Actualizados

### 1. Obtener tareas con filtrado por etiquetas
```
GET /tasks?tags=urgente,trabajo
Authorization: Bearer <token>
```

**Parámetros de consulta:**
- `tags` (opcional): Lista de etiquetas separadas por coma

### 2. Crear tarea con etiquetas
```
POST /tasks/create
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Completar proyecto",
  "description": "Finalizar el proyecto de la API",
  "status": "pending",
  "tag_names": ["urgente", "trabajo", "proyecto"]
}
```

### 3. Actualizar tarea con etiquetas
```
PUT /tasks/update/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Completar proyecto",
  "description": "Finalizar el proyecto de la API",
  "status": "completed",
  "tag_names": ["completado", "trabajo"]
}
```

## Tecnologías Utilizadas

- **FastAPI**: Framework web para la API
- **SQLAlchemy**: ORM para la base de datos
- **Alembic**: Migraciones de base de datos
- **PostgreSQL**: Base de datos
- **Pydantic**: Validación de datos y esquemas
- **JWT**: Autenticación

## Estructura del Proyecto

```
ToDo-FastAPI/
├── models/
│   ├── task.py      # Modelo Task con relacion a tags
│   ├── tag.py       # Modelo Tag y tabla intermedia
│   └── user.py      # Modelo User
├── schemas/
│   ├── task.py      # Esquemas Pydantic para Task
│   ├── tag.py       # Esquemas Pydantic para Tag
│   └── user.py      # Esquemas Pydantic para User
├── routes/
│   ├── task.py      # Endpoints de tareas con filtrado
│   ├── tag.py       # Endpoints CRUD de etiquetas
│   └── user.py      # Endpoints de usuarios
├── alembic/         # Migraciones de base de datos
└── app.py          # Aplicación principal
```

---

¡El sistema de etiquetas está completamente funcional y listo para usar! 🎉 
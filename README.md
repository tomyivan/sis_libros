# 📚 Sistema de Recomendación de Libros

Un sistema completo de recomendación de libros con autenticación segura y interfaz web moderna.

## 🚀 Características

- ✅ **Autenticación completa** con JWT y sesiones
- ✅ **Pantalla de login** moderna y responsive 
- ✅ **Dashboard interactivo** después del login
- ✅ **Protección de rutas** - todos los endpoints requieren autenticación
- ✅ **Validación de datos** con Marshmallow
- ✅ **Arquitectura hexagonal** bien estructurada
- ✅ **Base de datos MongoDB**
- ✅ **Interfaz Bootstrap** moderna

## 📋 Prerrequisitos

- Python 3.8+
- MongoDB running locally
- Git

## 🔧 Instalación

1. **Clonar el repositorio** (si aplica)
```bash
git clone [url-del-repo]
cd Sis_recomendacion_libros
```

2. **Crear entorno virtual**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
# Copiar el archivo de ejemplo
copy .env.example .env

# Editar .env con tus configuraciones
MONGO_URI=mongodb://localhost:27017/
SECRET_KEY=tu_clave_secreta_super_segura_aqui
JWT_SECRET_KEY=jwt_clave_secreta_aqui
```

5. **Iniciar MongoDB**
Asegúrate de que MongoDB esté ejecutándose localmente.

6. **Crear usuario administrador**
```bash
python create_admin_user.py
```

7. **Poblar base de datos con libros de ejemplo** (Opcional)
```bash
python seed_books.py
```

## 🚀 Ejecutar la aplicación

```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

## 🔐 Credenciales por defecto

- **Usuario:** `admin`
- **Contraseña:** `admin123`

> ⚠️ **IMPORTANTE:** Cambia la contraseña después del primer login

## 📱 Cómo usar

### 1. **Acceso inicial**
- Navega a `http://localhost:5000`
- Serás redirigido automáticamente al login
- Usa las credenciales por defecto

### 2. **Dashboard**
Una vez autenticado, tendrás acceso a:
- Panel principal con estadísticas
- Navegación por módulos
- Acciones rápidas
- Información de la sesión

### 3. **APIs Protegidas**
Todos los endpoints de `/usuario/*` requieren autenticación:

#### Para usar con token (APIs):
```bash
# 1. Hacer login y obtener token
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"alias": "admin", "password": "admin123"}'

# 2. Usar el token en las APIs
curl -X GET http://localhost:5000/usuario/obtener \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

#### Endpoints de Usuarios:
- `GET /usuario/obtener` - Listar usuarios
- `GET /usuario/obtener/<id>` - Obtener usuario específico  
- `POST /usuario/crear` - Crear nuevo usuario
- `PUT /usuario/actualizar` - Actualizar usuario
- `DELETE /usuario/desactivar` - Desactivar usuario

#### Endpoints de Libros:
- `GET /libro/obtener` - Listar libros con filtros
- `GET /libro/obtener/<id>` - Obtener libro específico
- `POST /libro/crear` - Crear nuevo libro
- `PUT /libro/actualizar/<id>` - Actualizar libro
- `DELETE /libro/eliminar/<id>` - Eliminar libro
- `PUT /libro/reactivar/<id>` - Reactivar libro
- `GET/POST /libro/buscar` - Buscar libros por texto
- `GET /libro/genero/<genero>` - Libros por género
- `GET /libro/autor/<autor>` - Libros por autor
- `GET /libro/mejor-calificados` - Libros mejor calificados
- `POST /libro/calificar/<id>` - Calificar libro
- `GET /libro/estadisticas` - Estadísticas de libros

## 🏗️ Estructura del proyecto

```
src/
├── app/                    # Servicios de aplicación
├── dominio/               # Lógica de dominio
│   ├── modelos/          # Entidades y DTOs
│   ├── puertos/          # Interfaces
│   └── servicios/        # Servicios de dominio
├── infrastuctura/        # Capa de infraestructura
│   ├── http/            # Controladores y rutas
│   │   ├── autenticacion/  # Sistema de auth
│   │   └── usuario/       # Módulo de usuarios
│   └── repositorio/      # Repositorios de datos
├── helpers/              # Conexiones y utilidades
└── template/            # Templates HTML
    ├── auth/           # Páginas de autenticación
    └── dashboard.html  # Dashboard principal
```

## 🔒 Seguridad implementada

- **Hashing de contraseñas** con bcrypt
- **JWT tokens** para APIs
- **Sesiones Flask** para web
- **Validación de inputs** con Marshmallow
- **Protección CSRF** en formularios
- **Headers de seguridad** configurados

## 🎨 Tecnologías usadas

- **Backend:** Flask, Python
- **Base de datos:** MongoDB
- **Frontend:** Bootstrap 5, HTML5, JavaScript
- **Autenticación:** JWT, bcrypt
- **Validación:** Marshmallow
- **Arquitectura:** Hexagonal (Ports & Adapters)

## 🐛 Troubleshooting

### Error de conexión MongoDB
```bash
# Verificar que MongoDB esté ejecutándose
# Windows:
net start MongoDB

# Linux/Mac:  
sudo systemctl start mongod
```

### Error de importaciones
```bash
# Verificar que estés en el directorio correcto
# y que el entorno virtual esté activado
pip install -r requirements.txt
```

### Token inválido
- Verifica que el `JWT_SECRET_KEY` sea el mismo en `.env`
- Verifica que el token no haya expirado (24 horas por defecto)

## 📝 Próximas características

- [ ] Registro de usuarios
- [ ] Recuperación de contraseña  
- [ ] Roles y permisos
- [ ] Sistema de recomendaciones ML
- [ ] API REST completa para libros
- [ ] Tests unitarios e integración

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo `LICENSE` para detalles.
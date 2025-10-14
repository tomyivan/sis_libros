"""
Script para crear un usuario administrador de prueba
Ejecutar: python create_admin_user.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.helpers.mongoconn_hlp import MongoConnection
from src.infrastuctura.repositorio.usuario_rep import UsuarioRepositorio
from src.dominio.modelos.usuario_mod import UsuarioModelo
from datetime import datetime
import bcrypt

def create_admin_user():
    try:
        # Conectar a la base de datos
        mongo_conn = MongoConnection()
        usuario_repo = UsuarioRepositorio(mongo_conn)
        
        # Datos del usuario administrador
        password = "admin123"  # Cambiar por una contraseña segura
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        admin_user = UsuarioModelo(
            nombre="Administrador",
            apellido="Sistema",
            alias="admin",
            email="admin@sistema.com",
            pais="Colombia",
            edad=30,
            password_hash=hashed_password,
            fecha_creacion=datetime.now(),
            activo=True,
            fecha_modificacion=datetime.now(),
            rol="admin"  # Rol de administrador
        )
        
        # Verificar si ya existe
        try:
            existing_user = usuario_repo.obtenerUsuarioPorAlias("admin")
            if existing_user:
                print("❌ El usuario administrador ya existe")
                return
        except:
            pass  # El usuario no existe, podemos crearlo
        
        # Crear el usuario
        result = usuario_repo.crearUsuario(admin_user)
        
        if result:
            print("✅ Usuario administrador creado exitosamente")
            print(f"   Alias: admin")
            print(f"   Contraseña: {password}")
            print(f"   Email: admin@sistema.com")
            print()
            print("🔐 IMPORTANTE: Cambia la contraseña después del primer login")
        else:
            print("❌ Error al crear el usuario administrador")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Creando usuario administrador...")
    create_admin_user()
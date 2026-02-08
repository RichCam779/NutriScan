import psycopg2
from fastapi import HTTPException
# Agregamos 'app.' al inicio para que Vercel encuentre los módulos
from app.config.db_config import get_db_connection
from app.models.user_model import User 
from fastapi.encoders import jsonable_encoder

class UserController:
    
    def create_user(self, user: User):   
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # 1. Insertamos en la tabla usuarios
            cursor.execute("""
                INSERT INTO usuarios (cedula, nombre_completo, email, telefono, genero, password_hash, id_rol) 
                VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id_usuario
            """, (user.cedula, user.nombre_completo, user.email, user.telefono, user.genero, user.password_hash, user.id_rol))
            
            new_id = cursor.fetchone()[0]
            
            # 2. Creamos el perfil clínico vacío
            cursor.execute("INSERT INTO perfiles_clinicos (id_usuario) VALUES (%s)", (new_id,))
            
            conn.commit()
            return {"resultado": "Usuario y Perfil creados con éxito", "id": new_id}
        
        except psycopg2.Error as err:
            if conn: conn.rollback()
            if err.pgcode == '23505': # Violación de unicidad
                raise HTTPException(status_code=400, detail="Error: Ya existe un usuario con esa cédula o email.")
            raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(err)}")
        finally:
            if conn: conn.close()

    def get_active_users(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                SELECT u.id_usuario, u.cedula, u.nombre_completo, u.email, u.telefono, u.genero, r.nombre_rol, p.biotipo, u.estado
                FROM usuarios u
                JOIN roles r ON u.id_rol = r.id_rol
                LEFT JOIN perfiles_clinicos p ON u.id_usuario = p.id_usuario
                WHERE u.estado = 'Activo'
            """
            cursor.execute(query)
            result = cursor.fetchall()
            
            payload = []
            for data in result:
                content = {
                    'id': data[0], 'cedula': data[1], 'nombre': data[2],
                    'email': data[3], 'telefono': data[4], 'genero': data[5],
                    'rol': data[6], 'biotipo': data[7], 'estado': data[8]
                }
                payload.append(content)
            
            return {"resultado": jsonable_encoder(payload)}
                
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn: conn.close()

    def deactivate_user(self, user_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE usuarios SET estado = 'Inactivo' WHERE id_usuario = %s", (user_id,))
            conn.commit()
            
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
                
            return {"resultado": "Cuenta de usuario desactivada correctamente"}
        except psycopg2.Error as err:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn: conn.close()

    def update_biotype(self, user_id: int, biotipo: str, confianza: float):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE perfiles_clinicos 
                SET biotipo = %s, confianza_ia = %s 
                WHERE id_usuario = %s
            """, (biotipo, confianza, user_id))
            conn.commit()
            return {"resultado": "Biotipo actualizado por IA"}
        except psycopg2.Error as err:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn: conn.close()

    def update_user(self, user: User):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE usuarios 
                SET nombre_completo = %s, email = %s, telefono = %s, genero = %s, password_hash = %s, id_rol = %s
                WHERE id_usuario = %s
            """, (user.nombre_completo, user.email, user.telefono, user.genero, user.password_hash, user.id_rol, user.id))
            
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            return {"resultado": "Usuario y Rol actualizados con éxito"}
        except psycopg2.Error as err:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn: conn.close()
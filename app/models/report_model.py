# app/models/report_model.py

from app import mysql

def insert_reporte(data):
    query = """
        INSERT INTO reportes_incidencias (folio, id_alumno, id_tipo_reporte, descripcion_hechos, acciones_tomadas, fecha_incidencia, estatus, id_usuario_que_reporta)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        data['folio'],
        data['id_alumno'],
        data['id_tipo_reporte'],
        data['descripcion_hechos'],
        data['acciones_tomadas'],
        data['fecha_incidencia'],
        data['estatus'],
        data['id_usuario_que_reporta']
    )

    cursor = mysql.connection.cursor()
    cursor.execute(query, values)
    mysql.connection.commit()
    cursor.close()
    



def get_all_reportes(estatus=None, tipo=None):
    query = """
        SELECT r.folio, r.fecha_incidencia, r.estatus,
               a.nombres AS alumno_nombre, a.apellido_paterno, a.apellido_materno,
               t.nombre AS tipo_reporte
        FROM reportes_incidencias r
        JOIN alumnos a ON r.id_alumno = a.id_alumno
        JOIN tipos_reporte t ON r.id_tipo_reporte = t.id_tipo_reporte
        WHERE 1=1
    """
    params = []
    if estatus:
        query += " AND r.estatus = %s"
        params.append(estatus)
    if tipo:
        query += " AND t.nombre = %s"
        params.append(tipo)

    query += " ORDER BY r.fecha_incidencia DESC"
    cursor = mysql.connection.cursor(dictionary=True)
    cursor.execute(query, params)
    reportes = cursor.fetchall()
    cursor.close()
    return reportes

def get_all_report():
    query = """
        SELECT r.folio, r.fecha_incidencia, r.estatus,
               a.nombres AS alumno_nombre, a.apellido_paterno, a.apellido_materno,
               t.nombre AS tipo_reporte
        FROM reportes_incidencias r
        JOIN alumnos a ON r.id_alumno = a.id_alumno
        JOIN tipos_reporte t ON r.id_tipo_reporte = t.id_tipo_reporte
        WHERE 1=1
    """
    
    #query += " ORDER BY r.fecha_incidencia DESC"
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    reportes = cursor.fetchall()
    cursor.close()
    return reportes

def get_tipos_reporte():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT nombre FROM tipos_reporte")
    tipos = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return tipos


def get_alumnos():
    query = "SELECT id_alumno, nombres, apellido_paterno, apellido_materno FROM alumnos"
    cursor = mysql.connection.cursor(dictionary=True)
    cursor.execute(query)
    alumnos = cursor.fetchall()
    cursor.close()
    return alumnos

def get_grupos():
    query = "SELECT id_grupo, grado, Descripcion, ciclo_escolar, id_tutor FROM grupos"
    cursor = mysql.connection.cursor(dictionary=True)
    cursor.execute(query)
    grupos = cursor.fetchall()
    cursor.close()
    return grupos

def get_tipos_reporte():
    query = "SELECT id_tipo_reporte, nombre FROM tipos_reporte"
    cursor = mysql.connection.cursor(dictionary=True)
    cursor.execute(query)
    tipos = cursor.fetchall()
    cursor.close()
    return tipos

def generar_folio():
    from datetime import datetime
    import random

    año = datetime.now().year
    numero = random.randint(1000, 9999)
    return f"REP-{año}-{numero}"

def generar_folio_incremental():
    from datetime import datetime

    año = datetime.now().year
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT folio FROM reportes_incidencias WHERE folio LIKE %s ORDER BY folio DESC LIMIT 1", (f"REP-{año}-%",))
    resultado = cursor.fetchone()
    cursor.close()

    if resultado:
        ultimo_folio = resultado[0]  # Ej: 'REP-2025-0042'
        numero = int(ultimo_folio.split('-')[-1]) + 1
    else:
        numero = 1

    return f"REP-{año}-{numero:04d}"

def get_reporte_por_folio(folio):
    query = """
        SELECT r.*, a.nombres, a.apellido_paterno, a.apellido_materno,
               t.nombre AS tipo_reporte
        FROM reportes_incidencias r
        JOIN alumnos a ON r.id_alumno = a.id
        JOIN tipos_reporte t ON r.id_tipo_reporte = t.id
        WHERE r.folio = %s
    """
    cursor = mysql.connection.cursor(dictionary=True)
    cursor.execute(query, (folio,))
    reporte = cursor.fetchone()
    cursor.close()
    return reporte



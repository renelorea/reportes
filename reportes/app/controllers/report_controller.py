

from app.models.report_model import insert_reporte, get_all_reportes, get_all_report

def create_report(form_data):
    data = {
        "folio": form_data["folio"],
        "id_alumno": int(form_data["id_alumno"]),
        "id_usuario_que_reporta": int(form_data["id_usuario"]),
        "id_tipo_reporte": int(form_data["id_tipo"]),
        "descripcion_hechos": form_data["descripcion"],
        "acciones_tomadas": form_data["acciones"],
        "fecha_incidencia": form_data["fecha"],
        "estatus": form_data["estatus"]
    }
    insert_reporte(data)

def fetch_reportes():
    return get_all_report()

def fetch_report(estatus,tipo):
    return get_all_reportes(estatus,tipo)


from flask import Blueprint, render_template, request, redirect, url_for, make_response
import pdfkit
from app.controllers.report_controller import create_report, fetch_reportes, fetch_report
from app.models.report_model import get_alumnos, get_tipos_reporte, get_reporte_por_folio, get_grupos

report_bp = Blueprint('report_bp', __name__, url_prefix='/reportes')

from app.models.report_model import generar_folio_incremental

@report_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_reporte():
    if request.method == 'POST':
        create_report(request.form)
        return redirect(url_for('report_bp.lista_reportes'))

    alumnos = get_alumnos()
    tipos = get_tipos_reporte()
    folio = generar_folio_incremental()
    grupos = get_grupos()
    return render_template('reportes/nuevo_reporte.html', grupos=grupos, alumnos=alumnos, tipos=tipos, folio=folio)

@report_bp.route('/listaReportes')
def lista_reportes():
    estatus = request.args.get('estatus')
    tipo = request.args.get('tipo')
    reportes = fetch_report(estatus, tipo)
    tipos = get_tipos_reporte()
    return render_template('reportes/lista_reportes.html', reportes=reportes, tipos=tipos)


@report_bp.route('/<folio>')
def ver_reporte(folio):
    reporte = get_reporte_por_folio(folio)
    return render_template('reportes/detalle_reporte.html', reporte=reporte)

@report_bp.route('/exportar_pdf')
def exportar_pdf():
    reportes = fetch_reportes()
    rendered = render_template('reportes/pdf_template.html', reportes=reportes)
    pdf = pdfkit.from_string(rendered, False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=reportes.pdf'
    return response

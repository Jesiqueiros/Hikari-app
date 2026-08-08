from django.db import connection
from django.utils import timezone
from datetime import timedelta
from nucleo.choices import MetodoPago, EstadoPago
from administracion.models import PagoSesion, Gasto
from citas.models import Cita

from django.db.models import F, Value, FloatField, ExpressionWrapper, CharField
from django.db.models.functions import Concat


# Valores para filtrar
transferencia = MetodoPago.TRANSFERENCIA
efectivo = MetodoPago.EFECTIVO

def current_day():
    
    today = timezone.now()
    
    year, week,_ = today.isocalendar()

    fecha_historica = today.date() - timedelta(weeks=4)
    
    return year, week, fecha_historica

def query(sql, params=None):
    """Ejecuta una consulta SQL y devuelve una lista de diccionarios."""

    with connection.cursor() as cursor:
        cursor.execute(sql, params or [])
        
        # Fetch column names from the cursor description 
        columns = [col[0] for col in cursor.description]
        
        # Combine column names and row values into a list of dictionaries
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return results
    
def metrica_ingresos():
    
    TR = MetodoPago.TRANSFERENCIA
    EF = MetodoPago.EFECTIVO
    
    year, week, _ = current_day()

    sql = """
        select
            sum(case when metodo_pago = %s then monto else 0 end) as transferencia,
            sum(case when metodo_pago = %s then monto else 0 end) as efectivo,
            sum(monto) as total
        from pago_sesiones
        where
            extract(WEEK from fecha) = %s
            AND extract(year from fecha) = %s
    """

    return query(sql, [TR, EF, week, year])[0]

def metrica_gastos():
    TR = MetodoPago.TRANSFERENCIA
    EF = MetodoPago.EFECTIVO

    sql = """
        select
            sum(case when metodo_pago = %s then monto else 0 end) as transferencia,
            sum(case when metodo_pago = %s then monto else 0 end) as efectivo,
            sum(monto) as total
        from gastos
        where estado_pago != 'PAGADO';
        """
    return query(sql, [TR, EF])[0]

    
def datos_grafico_contabilidad():

    _, _, fecha_inicio = current_day()

    sql = """
        SELECT
            date_trunc('week', fecha)::date AS semana,
            SUM(ingresos) AS ingresos,
            SUM(gastos) AS gastos
        FROM (
            SELECT
                fecha,
                monto AS ingresos,
                0 AS gastos
            FROM pago_sesiones
            WHERE fecha >= %s

            UNION ALL

            SELECT
                fecha,
                0 AS ingresos,
                monto AS gastos
            FROM gastos
            WHERE fecha >= %s
        ) movimientos
        GROUP BY
            date_trunc('week', fecha)
        ORDER BY
            date_trunc('week', fecha);
    """

    return query(sql, [fecha_inicio, fecha_inicio])


def tabla_anexo_ingreso():
    # get current date
    year, week, _ = current_day()
    
    # Constuir queries
    ingresos = PagoSesion.objects \
        .filter(fecha__week=week, fecha__year=year) \
        .all()
        
    return ingresos
        
def tabla_anexo_gastos():
    # Construir query
    gastos = Gasto.objects.exclude(estado_pago=EstadoPago.PAGADO).all()
    return gastos
    

def consultas_cobradas(terapeuta_id=None):

    citas = Cita.objects.filter(
        liquidada=False,
        pago__isnull=False,
    )

    if terapeuta_id:
        citas = citas.filter(terapeuta_id=terapeuta_id)

    return (
        citas
        .annotate(
            monto=ExpressionWrapper(
                F("pago__monto") / F("pago__sesiones_cubiertas"),
                output_field=FloatField(),
            )
        )
        .values(
            "monto",
            fecha_cita=F("fecha"),
            hora_cita=F("hora"),
            nombre_paciente=F("paciente__nombre"),
            nombre_terapeuta=F("terapeuta__nombre"),
            metodo_pago=F("pago__metodo_pago"),
        )
    )
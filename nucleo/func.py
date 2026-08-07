from .choices import EstadoCita

def ColorCita(status):
    if status == EstadoCita.AGENDADO:
        return'#00FF00'
    elif status == EstadoCita.CONSULTADO:
        return '#0000FF'
    else:
        return '#FF0000'
    
def construir_mensaje(paciente, fechas):

    plural = len(fechas) > 1

    return (
        f"Hola, buen día 🌈✨\n\n"
        f"Le compartimos la{'s fechas pendientes' if plural else ' fecha pendiente'} de *{paciente}*:\n\n"
        f"• " + "\n• ".join(fechas) +
        "\n\nAgradecemos su apoyo para realizar el pago y enviar su comprobante por este medio.\n\n"
        "Si ya fue cubierto, favor de omitir este mensaje 💫"
    )
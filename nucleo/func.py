from .choices import EstadoCita

def ColorCita(status):
    if status == EstadoCita.AGENDADO:
        return'#00FF00'
    elif status == EstadoCita.CONSULTADO:
        return '#0000FF'
    else:
        return '#FF0000'
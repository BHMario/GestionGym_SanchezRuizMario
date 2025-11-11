import re
from datetime import datetime
from .constantes import FORMATO_FECHA, FORMATO_HORA

def validar_email(email: str) -> bool:
    """Valida que el email tenga un formato correcto"""
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, email) is not None

def validar_telefono(telefono: str) -> bool:
    """Valida que el teléfono contenga solo números y tenga entre 7 y 15 dígitos"""
    return telefono.isdigit() and 7 <= len(telefono) <= 15

def validar_fecha(fecha: str) -> bool:
    """Valida que la fecha tenga el formato YYYY-MM-DD"""
    try:
        datetime.strptime(fecha, FORMATO_FECHA)
        return True
    except ValueError:
        return False

def validar_hora(hora: str) -> bool:
    """Valida que la hora tenga el formato HH:MM"""
    try:
        datetime.strptime(hora, FORMATO_HORA)
        return True
    except ValueError:
        return False

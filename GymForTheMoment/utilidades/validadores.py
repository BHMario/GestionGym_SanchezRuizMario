import re

def validar_email(email):
    """
    Valida un email usando expresión regular RFC 5322 simplificada.
    Retorna True si es válido, False en caso contrario.
    """
    patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(patron, email) is not None

def validar_usuario(usuario):
    """
    Valida un nombre de usuario:
    - Mínimo 3 caracteres
    - Máximo 20 caracteres
    - Solo letras, números y guiones bajos
    """
    if not usuario or len(usuario) < 3 or len(usuario) > 20:
        return False
    patron = r"^[a-zA-Z0-9_]+$"
    return re.match(patron, usuario) is not None

def validar_contrasena(contrasena):
    """
    Valida una contraseña:
    - Mínimo 6 caracteres
    - Debe contener al menos una letra y un número
    """
    if not contrasena or len(contrasena) < 6:
        return False
    tiene_letra = any(c.isalpha() for c in contrasena)
    tiene_numero = any(c.isdigit() for c in contrasena)
    return tiene_letra and tiene_numero

def validar_telefono(telefono):
    """
    Valida un número de teléfono:
    - Solo dígitos
    - Mínimo 9 dígitos
    """
    if not telefono:
        return False
    patron = r"^\d{9,}$"
    return re.match(patron, telefono) is not None

def validar_fecha(fecha_str):
    """
    Valida que una fecha sea en formato YYYY-MM-DD y sea válida.
    Retorna True si es válida, False en caso contrario.
    """
    try:
        import datetime
        datetime.datetime.strptime(fecha_str, "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        return False


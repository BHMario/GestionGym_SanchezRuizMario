from utilidades.validadores import validar_email

class Validaciones:
    @staticmethod
    def es_email_valido(email: str) -> bool:
        """Valida formato de email usando utilidades generales"""
        return validar_email(email)

    @staticmethod
    def campo_no_vacio(campo: str) -> bool:
        """Verifica que el campo no esté vacío"""
        return bool(campo and campo.strip())

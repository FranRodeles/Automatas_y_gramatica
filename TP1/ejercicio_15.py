'''
Escribir una expresión regular que valide una dirección de mail según estas reglas:
• Nombre de usuario: letras mayúsculas, minúsculas, números y solo los caracteres
especiales guion medio ( - ) y guion bajo ( _ ).
• Debe haber exactamente un símbolo @ separando usuario y dominio.
• Dominio: solo letras mayúsculas, minúsculas y números (sin caracteres especiales).
• Extensión: entre 2 y 4 letras (ej: .com, .org, .edu, .info).
'''
import re

def validacion_email(email):
    patron_email = r'^[a-zA-Z]+[a-zA-Z0-9_-]*@[a-zA-Z0-9]+\.[a-zA-Z]{2,4}$'
    return re.match(patron_email, email) is not None

# Ejemplo de uso
emails = [ "user@example.com", "invalid.email", "test_user@domain.org", "another_user@sub.domain.edu", 
          "bad-email@domain", "user@domain.c", "15edu@domain.info", "validemail178_78@domain.edu",
           "invalid-email@domain..com", "Hagrid@hot_mail.com "]

for email in emails:
    print(f"{email}: {'Válido' if validacion_email(email) else 'Inválido'}")




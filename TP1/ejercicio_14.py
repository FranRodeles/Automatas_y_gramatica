'''
El departamento de historia está digitalizando documentos antiguos, pero el sistema generó mucha
"basura" alrededor de los datos importantes en el documento de texto. Les pidieron extraer todas las
fechas mencionadas en un párrafo extenso. Saben que las fechas buscadas están escritas siempre
en el formato estricto DD/MM/YYYY. Escriban un programa utilizando el módulo re que busque y
devuelva una lista con todas las ocurrencias que coincidan con este formato dentro del texto masivo.
Investiguen qué función específica de las expresiones regulares en Python sirve para encontrar y
extraer múltiples coincidencias.
Input de ejemplo:
"El acta original fue redactada el 15/04/1815 y posteriormente ratificada el 09/07/1816 en la
asamblea. Se descartó por completo el borrador del 2/5/1814 por falta de firmas."
Output esperado:
['15/04/1815', '09/07/1816']. 
'''
import re 

def es_bisiesto(anio):
    return anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)


def fecha_valida(dia, mes, anio):
    # Devuelve True si la fecha existe en el calendario, False en caso contrario
    dias_por_mes = {
        1: 31,
        2: 29 if es_bisiesto(anio) else 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31,
    }

    # Primero validamos el mes para evitar usar una clave inexistente en el diccionario
    if not 1 <= mes <= 12:
        return False

    # Si el mes es valido, validamos que el dia este dentro del rango permitido
    return 1 <= dia <= dias_por_mes[mes]


def extraer_fechas(texto):
    # Expresión regular para encontrar fechas en formato DD/MM/YYYY
    patron_fecha = r'\b\d{2}/\d{2}/\d{4}\b'
    
    # Utilizamos re.findall para extraer todas las coincidencias
    fechas_encontradas = re.findall(patron_fecha, texto)

    fechas_validas = []
    for fecha in fechas_encontradas:
        # COnvertimos a numero para hacer verificaciones en las funciones de validacion
        dia_str, mes_str, anio_str = fecha.split('/')
        dia = int(dia_str)
        mes = int(mes_str)
        anio = int(anio_str)

        if fecha_valida(dia, mes, anio):
            fechas_validas.append(fecha)

    return fechas_validas

# Ejemplo de uso
texto = " 03/02/2023, 31/02/1815, 31,02/1815, 31/04/1254, 15/13/1456"

fechas = extraer_fechas(texto)
print(fechas)

























'''Imaginen que el sistema de alumnos recibió inscripciones a las mesas de exámenes, pero los
nombres ingresados tienen un formato caótico. Algunos están en mayúsculas, otros en minúsculas
y muchos contienen espacios extra innecesarios al principio o al final de la cadena. Escriban una
función que reciba uno de estos strings desordenados y lo devuelva en formato "Título" (solo la
primera letra en mayúscula), eliminando cualquier espacio sobrante en los extremos. Exploren los
métodos nativos que los objetos string de Python ya nos ofrecen para limpiar y transformar texto
sin usar librerías externas.
Input de ejemplo:
" JUAN pablo DOMINGUEZ"
Output esperado:
"Juan Pablo Dominguez"
    '''
import re
entrada = "JUAN pablo DOMINGUEZ "
def limpiar_nombre(entrada):
    Nombre_corregido = entrada.strip().title()
    return Nombre_corregido
resultado= limpiar_nombre(entrada)
print(resultado)
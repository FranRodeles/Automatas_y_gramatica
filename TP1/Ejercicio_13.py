"""El estacionamiento de la universidad está implementando un sistema de cámaras para lectura
automática de patentes y necesitan un programa que filtre las lecturas erróneas de la cámara. Deben
validar el formato de las patentes del Mercosur utilizadas en Argentina, que consisten exactamente
en dos letras, seguidas de tres números y terminando con dos letras más (ejemplo: AB123CD).
Escriban una función utilizando la librería re que verifique si una cadena cumple estrictamente con
este patrón de inicio a fin.."""

import re

def validar_patente(patente):
    patron = r'^[A-Za-z]{2}[0-9]{3}[A-Za-z]{2}$'

    if re.match(patron, patente):
        return True
    else:
        return False

print(validar_patente("AA254BC"))  # True
print(validar_patente("A21B"))     # False


"""El administrador de redes de la facultad necesita su ayuda. Les entregó un archivo de texto llamado
servidores.txt que contiene un listado enorme de direcciones IP y nombres de equipos. Sin embargo,
muchas de las líneas están comentadas (comienzan con el símbolo #) porque esos equipos están
dados de baja, o simplemente son líneas en blanco. Construyan un script que lea este archivo y
genere uno nuevo llamado activos.txt que contenga únicamente los servidores en funcionamiento.
Recuerden cómo abrir archivos en modo lectura y escritura, y cómo iterar sobre ellos.
Input de servidores.txt:
# Listado de servidores 2026
192.168.0.101 Servidor_Web_Principal
# 192.168.0.102 Servidor_Web_Backup
192.168.0.105 Base_de_Datos_1
192.168.0.106 Base_de_Datos_2_Replica
# Infraestructura Interna y Redes
192.168.0.110 DNS_Primario
# 192.168.0.111 DNS_Secundario_Viejo
192.168.0.112 Controlador_Dominio
192.168.0.115 Proxy_Autenticacion
# Servicios de la Facultad
192.168.1.50 Sistema_Alumnos_API
192.168.1.51 Campus_Virtual_Moodle
# 192.168.1.52 Campus_Virtual_Test
192.168.1.60 Servidor_Archivos_Docentes
192.168.1.65 Sistema_Biblioteca_Koha
# 192.168.1.70 Servidor_Impresion_Lab """

import re
import os

OUTPUT_DIR = "tp1"
os.makedirs(OUTPUT_DIR, exist_ok=True)

origen = os.path.join(OUTPUT_DIR, 'servidores.txt')
destino = os.path.join(OUTPUT_DIR, 'activos.txt')
with open(origen, 'r', encoding='utf-8') as f_in, \
    open(destino, 'w', encoding='utf-8') as f_out:
    
    for linea in f_in:
        linea_limpia = linea.strip()
        if linea_limpia and not linea_limpia.startswith('#'):
            f_out.write(linea_limpia + '\n')

print(f"--- Archivo '{destino}' generado con éxito ---")

print("\nContenido de servidores activos:")
print("-" * 40) 

with open(destino, 'r', encoding='utf-8') as f_final:
    print(f_final.read())

print("-" * 40)

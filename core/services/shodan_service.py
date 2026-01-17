import shodan
import socket
from django.conf import settings
from core.models import ActivoDigital

def buscar_ip_shodan(ip):
    """
    Consulta OSINT pasiva en Shodan por IP pública
    """
    api = shodan.Shodan(settings.SHODAN_API_KEY)

    try:
        resultado = api.host(ip)
        return resultado
    except shodan.APIError as e:
        return {"error": str(e)}


def crear_activos_desde_shodan(ip, proyecto):
    api = shodan.Shodan(settings.SHODAN_API_KEY)
    activos_creados = []

    try:
        resultado = api.host(ip)

        # Activo IP pública
        activo_ip, creado = ActivoDigital.objects.get_or_create(
            proyecto=proyecto,
            nombre=resultado.get('ip_str'),
            defaults={
                'tipo': 'IP Pública',
                'descripcion': f"IP detectada por Shodan. Org: {resultado.get('org')}",
                'c': 3,
                'i': 3,
                'd': 4,
                'nivel_criticidad': 'Media',
                'fuente_osint': 'Shodan',
                'estado': 'Activo'
            }
        )

        if creado:
            activos_creados.append(activo_ip)


        # Activos por servicio/puerto
        for servicio in resultado.get('data', []):
            nombre_activo = f"{ip}:{servicio.get('port')}"

            if not ActivoDigital.objects.filter(
                proyecto=proyecto,
                nombre=nombre_activo
            ).exists():
                activo_servicio = ActivoDigital.objects.create(
                    proyecto=proyecto,
                    nombre=nombre_activo,
                    tipo='Servicio Expuesto',
                    descripcion=servicio.get('product', 'Servicio detectado'),
                    c=3,
                    i=3,
                    d=3,
                    nivel_criticidad='Media',
                    fuente_osint='Shodan',
                    estado='Activo'
                )
                activos_creados.append(activo_servicio)


        return activos_creados

    except shodan.APIError as e:
        return {"error": str(e)}

def resolver_objetivo(objetivo):
    try:
        return socket.gethostbyname(objetivo)
    except socket.gaierror:
        return None

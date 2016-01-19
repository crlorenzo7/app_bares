import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twdp.settings')

import django
django.setup()

from rango.models import Bares, Tapas


def populate():
    python_bar = add_bar('bagueton','Motril')

    add_tapa(bar=python_bar,nombre="Americano")
    add_tapa(bar=python_bar,nombre="pepito")
    add_tapa(bar=python_bar,nombre="planchita")

    python_bar = add_bar('Manhattan','Maracena')

    add_tapa(bar=python_bar,nombre="Harlem")
    add_tapa(bar=python_bar,nombre="Nueva York")
    add_tapa(bar=python_bar,nombre="Serranito")
    
    python_bar = add_bar('Me da igual','Maracena')

    add_tapa(bar=python_bar,nombre="hamburguesa")
    add_tapa(bar=python_bar,nombre="pinchitos")
    add_tapa(bar=python_bar,nombre="bikini")

    # Print out what we have added to the user.
    for c in Bares.objects.all():
        for p in Tapas.objects.filter(bar=c):
            print "- {0} - {1}".format(str(c), str(p))

def add_tapa(bar, nombre,votos=0):
    p = Tapas.objects.get_or_create(bar=bar, nombre=nombre)[0]
    p.votos=votos
    p.save()
    return p

def add_bar(nombre,direccion,numero_visitas=0):
    c = Bares.objects.get_or_create(nombre=nombre)[0]
    c.direccion=direccion
    c.numero_visitas=numero_visitas
    c.save()
    return c

# Start execution here!
if __name__ == '__main__':
    print "Starting Rango population script..."
    populate()
# Generated by Django 4.2.6 on 2023-12-03 01:30

from django.db import migrations

def create_products(apps, schema_editor):
    Product = apps.get_model('appPuraAqua', 'Product')
    products = [
        {'name': 'Agua 20 Litros', 'quantity': 100, 'price': 3500},
        {'name': 'Agua  10 Litros', 'quantity': 100, 'price': 2000},
        {'name': 'Agua  2 Litros', 'quantity': 100, 'price': 1000},
        # Agrega más productos aquí
        # no carga imagenes
    ]
    for product in products:
        Product.objects.create(**product)

def create_regions(apps, schema_editor):
    City = apps.get_model('appPuraAqua', 'City')
    cities = ['Santiago']  # Reemplaza esto con las regiones que usarás
    for city in cities:
        City.objects.create(name_city=city)  # Usa la variable 'city' aquí

def create_comunas(apps, schema_editor):
    Comuna = apps.get_model('appPuraAqua', 'Comuna')
    comunas = ['Santiago', 'Recoleta', 'Independencia', 'La Florida', 'Puente Alto', 'Maipú', 'Peñalolén', 'Providencia', 'Las Condes', 'Ñuñoa', 'Macul', 'La Cisterna', 'San Miguel', 'San Joaquín', 'La Granja', 'Quilicura', 'Pudahuel', 'Cerro Navia', 'Renca', 'Huechuraba', 'Conchalí', 'Quinta Normal', 'Estación Central', 'Cerrillos', 'Lo Espejo', 'Pedro Aguirre Cerda', 'Lo Prado', 'Peñaflor', 'Padre Hurtado', 'Lampa', 'Colina', 'Tiltil', 'San Ramón', 'La Pintana', 'El Bosque', 'La Reina', 'Lo Barnechea', 'Vitacura', 'Lampa', 'Calera de Tango', 'Buin', 'San Bernardo', 'Paine', 'Melipilla', 'Alhué', 'Curacaví', 'María Pinto', 'San José de Maipo', 'Pirque', 'Isla de Maipo', 'San Pedro', 'Cajón del Maipo']  # Corrige esto con las comunas que se usaran
    for comuna in comunas:
        Comuna.objects.create(name_comuna=comuna)

class Migration(migrations.Migration):

    dependencies = [
        ('appPuraAqua', '0001_initial'),  # Reemplaza '0001_initial' con el nombre de tu migración que crea el modelo Comuna
    ]

    operations = [
        migrations.RunPython(create_regions),
        migrations.RunPython(create_comunas),
        migrations.RunPython(create_products),
    ]
#0002_initial.py asi se debe llamar el nombre del archivo

# instrucciones para ejecutar la migracion
# python manage.py makemigrations
# python manage.py migrate
# luego debe mover el archivo 0002_initial.py a la carpeta migrations(que esta dentro de la app en la carpeta rellenarComunas)
# luego manage.py migrate
# con eso ya estaria cargada las 52 comunas de santiago


#usar la siguente linea para cargar todas las regiones
#regions = ['Región de Arica y Parinacota', 'Región de Tarapacá', 'Región de Antofagasta', 'Región de Atacama', 'Región de Coquimbo', 'Región de Valparaíso', 'Región Metropolitana de Santiago', 'Región del Libertador General Bernardo O’Higgins', 'Región del Maule', 'Región del Ñuble', 'Región del Biobío', 'Región de la Araucanía', 'Región de Los Ríos', 'Región de Los Lagos', 'Región de Aysén del General Carlos Ibáñez del Campo', 'Región de Magallanes y de la Antártica Chilena']  # Corrige esto con las regiones que se usaran
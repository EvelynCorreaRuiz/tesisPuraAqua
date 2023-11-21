from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

class User(AbstractUser):
    last_name2 = models.CharField(max_length=20)
    rut = models.CharField(max_length=12) #que cumpla formato 17103459-0
    phone = models.CharField(max_length=12) # que tenga por defento el +56 y el numero debe tener 9 por obligacion
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=20) # que solo muestre santiago y viña del mar
    numberAddress = models.CharField(max_length=10)
    birthdate = models.DateField(default=date.today) #asegurar que sea mayo de 18

""" Dirección de correo electrónico: 
- Debe asegurarse de que se proporciona una dirección de correo válida.  
- El sistema debe garantizar que la dirección de correo electrónico proporcionada sea única y no esté asociada con otra cuenta registrada. 
"""

"""la password Contraseña: 
- Debe tener un mínimo de 12 caracteres. 
- Debe contener al menos una letra mayúscula. 
- Debe contener al menos un número. 
- Debe contener al menos un carácter especial ( !, @, etc.). """

"""Confirmación de Registro: 
Se debe generar una confirmación de registro o un correo electrónico de bienvenida 
después de que el usuario complete el proceso de registro con éxito. 
"""

# debe logear con el correo electronico y la contraseña

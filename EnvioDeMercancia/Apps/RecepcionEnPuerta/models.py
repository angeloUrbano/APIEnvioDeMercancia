from django.db import models
from simple_history.models import HistoricalRecords



class CajasAlmacenadas(models.Model):
    
    numeroTracking = models.CharField("numero de traking" , max_length=200)
    fecha_hora = models.DateTimeField("fecha creacion de registro" , auto_now_add=True)
    wareHouseCreated = models.BooleanField("werehouse creado" , default=False)
    is_active = models.BooleanField("activo" , default=True)
    historical = HistoricalRecords()


    def __str__(self):
        return f'{self.numeroTracking} , {self.fecha_hora}'

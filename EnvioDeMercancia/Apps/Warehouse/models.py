# from django.db import models

# # Create your models here.



# class wareHouse(models.Model):
#     MY_CHOICES =(
#         ("Persona" , "Persona Natural"),
#         ("Empresa" , "Persona Juridica")
#     )

#     MY_CHOICES2 =(
#         ("1" , 1),
#         ("2" , 2)
#     )
#     tipo_de_persona = models.CharField(max_length=60 , choice=MY_CHOICES)
#     shipper = models.CharField(max_length=150 , blank=True , null=False)
#     recibido_de = models.CharField(max_length=150 , blank=False , null=False)
#     persona_recibe = models.CharField(max_length=150 , null=False , blank=False)
#     peso_caja = models.FloatField()
#     ancho_caja = models.FloatField()
#     profundida_caja = models.FloatField()
#     pago = models.FloatField()
#     registro_cliente = models.ForeignKey(RegistroCliente , verbose_name=("registro cliente") , on_delete=models.CASCADE)
#     traking_num = models.IntegerChoices(choice = MY_CHOICES2)
#     usuario = models.ForeignKey(Usuario , on_delete=models.CASCADE)
#     contenido = models.TextField()
#     observaciones = models.TextField()

#     def __str__(self):
#         return f'{self.recibido_de} - {self.observaciones}'


# class Carrito(models.Model):
#     usuario = models.ForeignKey(Usuario , on_delete=models.CASCADE)
#     wareHouse = models.ForeignKey(wareHose , related_name="carritos")
#     fecha_creacion = models.DateTimeField(auto_created=False , auto_now=False)
#     cambio_de_persona = models.DateTimeField()

#     def __str__(self):
#         return f'carrito de {self.usuario.username} - {self.fecha_creacion}'



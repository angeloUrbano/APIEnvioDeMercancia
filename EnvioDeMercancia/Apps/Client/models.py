from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


from simple_history.models import HistoricalRecords




# Create your models here.




"""""  

dos tipos de clientes ?

1) el 90 % de la mercancia se compra online y las personas la envian a travez de empresas

2) la otra forma es una persona natural llevando la mercancia.



campos de clientes:

nombre
apellido
identificacion
direccion
correo
correo aux
tlefono
telefono aux


hay dos modulos de entrada:


debe terner dos modulos de acceso de entrada 

cuando la persona la lleva se le debe pedir quien envia y quien recibe
el otro caso solo se le carga la informacion de laque compro onlineremoterem

cuando la persona lo lleva directamente , en ese caso se debe registrar la informacion del destinatario etc

y cuando llega por un currier interno se registra la informacion que viene en la etiqueta


si es una persona natural tengo que registrar quien envia y quien recibe y esa informacion va en el mismo registro del clientes


cuando registrar un cliente le das un numero de registro para que todos los clientes tenga un numero asignado
pero ese codigo se tienen que sentar a diseñarlo junto con el amigo del señor iban , cuando registras el clientes
debes crear ese codigo , no es el id del cliente , es un codigo compuesto con el pais ,el estado , identificacion etc 


tanto para la empresa que lleva la caja o la persona natural se registra la misma informacion 

si lo lleva la empresa se registra de la etiqueta
si lo lleva una persona se le toman sus datos pero son los mismos

"""""




# model related to ClientCourier
class ClienteUsuarioDestino(models.Model):
    nombre = models.CharField(verbose_name='Nombre del cliente',max_length = 150, blank= False, null=False)
    apellido = models.CharField(verbose_name='Apellido del cliente',max_length = 150, blank= True, null=True)
    identificacion = models.CharField(verbose_name='identificacion' , unique=True ,max_length = 150, blank= True, null=True)
    correo = models.EmailField(verbose_name='correo', max_length=254, unique=True , blank= True, null=True)
    correo_aux = models.EmailField( verbose_name='correo aux',  max_length=254, unique=True , blank= True, null=True)
    telefono = models.CharField(max_length = 20 , blank= True, null=True , validators=[
            RegexValidator(
                regex=r'^\+?[0-9\s\-]+$',  # Permite: +, dígitos, espacios y guiones
                                message="Ingrese un número telefónico válido (ej: +1234567890 o 1234567890)")])
    telefono_aux =models.CharField(max_length = 20 , blank= True, null=True , validators=[
            RegexValidator(
                regex=r'^\+?[0-9\s\-]+$',  # Permite: +, dígitos, espacios y guiones
                                message="Ingrese un número telefónico válido (ej: +1234567890 o 1234567890)")])
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default = True)
    historical = HistoricalRecords()



    def __str__(self):
        return f"{self.nombre}, {self.apellido}"
    


# model related to ClientNatural
class ClienteQuienEnvia(models.Model):
    nombre = models.CharField(verbose_name='Nombre del cliente',max_length = 150, blank= False, null=False)
    apellido = models.CharField(verbose_name='Apellido del cliente',max_length = 150, blank= True, null=True)
    identificacion = models.CharField(verbose_name='identificacion' , unique=True ,max_length = 150, blank= False, null=False)
    correo = models.EmailField(verbose_name='correo',max_length=254, unique=True , blank= False, null=False)
    correo_aux = models.EmailField(verbose_name='correo aux',max_length=254, unique=True , blank= True, null=True)
    telefono = models.CharField(max_length = 20 , blank= True, null=True , validators=[
            RegexValidator(
                regex=r'^\+?[0-9\s\-]+$',  # Permite: +, dígitos, espacios y guiones
                                message="Ingrese un número telefónico válido (ej: +1234567890 o 1234567890)")])
    telefono_aux = models.CharField(max_length = 20 , blank= True, null=True , validators=[
            RegexValidator(
                regex=r'^\+?[0-9\s\-]+$',  # Permite: +, dígitos, espacios y guiones
                                message="Ingrese un número telefónico válido (ej: +1234567890 o 1234567890)")])
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default = True)
    historical = HistoricalRecords()

    
    def __str__(self):
        return f"{self.nombre}, {self.apellido}"
    


# model related to ClientNatural
class ClienteQuienRecibe(models.Model):
    nombre = models.CharField(verbose_name='Nombre del cliente',max_length = 150, blank= False, null=False)
    apellido = models.CharField(verbose_name='Apellido del cliente',max_length = 150, blank= True, null=True)
    identificacion = models.CharField(verbose_name='identificacion', unique=True , max_length = 150, blank= True, null=True)
    correo = models.EmailField(verbose_name='correo',max_length=254, unique=True , blank= True, null=True)
    correo_aux = models.EmailField(verbose_name='correo aux',max_length=254, unique=True , blank= True, null=True)
    telefono = models.CharField(max_length = 20 , blank= True, null=True , validators=[
            RegexValidator(
                regex=r'^\+?[0-9\s\-]+$',  # Permite: +, dígitos, espacios y guiones
                                message="Ingrese un número telefónico válido (ej: +1234567890 o 1234567890)")])
    telefono_aux =models.CharField(max_length = 20 , blank= True, null=True , validators=[
            RegexValidator(
                regex=r'^\+?[0-9\s\-]+$',  # Permite: +, dígitos, espacios y guiones
                                message="Ingrese un número telefónico válido (ej: +1234567890 o 1234567890)")])
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default = True)
    historical = HistoricalRecords()

    def __str__(self):
        return f"{self.nombre}, {self.apellido}" 
    
    


#this client is not a company
class ClientNatural(models.Model):
    nombre = models.CharField(verbose_name='Nombre del cliente',max_length = 150, blank= False, null=False)
    apellido = models.CharField(verbose_name='Apellido del cliente',max_length = 150, blank= True, null=True)
    identificacion = models.CharField(verbose_name='identificacion' , unique=True ,max_length = 150, blank= False, null=False)
    correo = models.EmailField(verbose_name='correo',max_length=254, unique=True , blank= False, null=False)
    correo_aux = models.EmailField(verbose_name='correo aux',max_length=254, unique=True , blank= True, null=True)
    telefono =models.CharField(max_length = 20 , blank= True, null=True , validators=[
            RegexValidator(
                regex=r'^\+?[0-9\s\-]+$',  # Permite: +, dígitos, espacios y guiones
                                message="Ingrese un número telefónico válido (ej: +1234567890 o 1234567890)")])
    telefono_aux = models.CharField(max_length = 20 , blank= True, null=True , validators=[
            RegexValidator(
                regex=r'^\+?[0-9\s\-]+$',  # Permite: +, dígitos, espacios y guiones
                                message="Ingrese un número telefónico válido (ej: +1234567890 o 1234567890)")])
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    # en caso que sea la persona perse que lleva la mercancia
    quien_envia = models.OneToOneField(ClienteQuienEnvia , verbose_name='Nombre de quien env la mercancia' , on_delete=models.CASCADE  , blank= False, null=False)
    quien_recibe = models.OneToOneField(ClienteQuienRecibe , verbose_name= 'Nombre de quien rcb la mercancia' , on_delete=models.CASCADE , blank= False, null=False)
    codigo_cliente = models.CharField(verbose_name="codigo de cliente" , max_length=200, blank= False, null=False )
    is_active = models.BooleanField(default = True)
    historical = HistoricalRecords()


    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()
        if self.quien_envia:
            self.quien_envia.is_active = False
            self.quien_envia.save()
            self.quien_envia.direcciones_quien_envia.update(is_active=False)
        
        if self.quien_recibe:
            self.quien_recibe.is_active = False
            self.quien_recibe.save()
            self.quien_recibe.direcciones_quien_recibe.update(is_active=False)
        
        self.direcciones_cliente_natural.update(is_active=False)
        
        return super().delete(*args, **kwargs) if kwargs.get('hard_delete', False) else None
    

    # con esta funcion revierto los cambios de la eliminacion logica
    def activate(self, *args, **kwargs):
        self.is_active = True
        self.save()
        if self.quien_envia:
            self.quien_envia.is_active = True
            self.quien_envia.save()
            self.quien_envia.direcciones_quien_envia.update(is_active=True)
        
        if self.quien_recibe:
            self.quien_recibe.is_active = True
            self.quien_recibe.save()
            self.quien_recibe.direcciones_quien_recibe.update(is_active=True)
        
        self.direcciones_cliente_natural.update(is_active=True)
        
        return super().delete(*args, **kwargs) if kwargs.get('hard_delete', False) else None




    def __str__(self):
        return f"{self.nombre}, {self.apellido}"
    

#this client is a company
class ClientCourier(models.Model):
    nombre = models.CharField(verbose_name='Nombre del cliente',max_length = 150, blank= False, null=False)
    apellido = models.CharField(verbose_name='Apellido del cliente',max_length = 150, blank= True, null=True)
    identificacion = models.CharField(verbose_name='identificacion', unique=True ,max_length = 150, blank= True, null=True)
    correo = models.EmailField(verbose_name='correo',max_length=254, unique=True , blank= True, null=True)
    correo_aux = models.EmailField(verbose_name='correo aux',max_length=254, unique=True , blank= True, null=True)
    telefono = models.CharField(max_length = 20 , blank= True, null=True , validators=[
            RegexValidator(
                regex=r'^\+?[0-9\s\-]+$',  # Permite: +, dígitos, espacios y guiones
                                message="Ingrese un número telefónico válido (ej: +1234567890 o 1234567890)")])
    telefono_aux = models.CharField(max_length = 20 , blank= True, null=True , validators=[
            RegexValidator(
                regex=r'^\+?[0-9\s\-]+$',  # Permite: +, dígitos, espacios y guiones
                                message="Ingrese un número telefónico válido (ej: +1234567890 o 1234567890)")])
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    # el valor de usuario_destino en este modelo se tiene que discutir con el cliente si se debe colocar o no
    usuario_destino = models.OneToOneField(ClienteUsuarioDestino ,verbose_name='Nombre de quien env la mercancia' , on_delete=models.CASCADE )

    codigo_cliente = models.CharField(verbose_name="codigo de cliente" , max_length=200, blank= False, null=False )
    is_active = models.BooleanField(default = True)
    historical = HistoricalRecords()

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()
    
        if self.usuario_destino:
            self.usuario_destino.is_active = False
            self.usuario_destino.save()
            self.usuario_destino.direcciones_destino.update(is_active=False)
        
        self.direcciones_cliente_courier.update(is_active=False)
        
        return super().delete(*args, **kwargs) if kwargs.get('hard_delete', False) else None
    
    #funcion para activar lo que se desactivo ern el eliminado logico
    def activate(self, *args, **kwargs):
        self.is_active = True
        self.save()
    
        if self.usuario_destino:
            self.usuario_destino.is_active = True
            self.usuario_destino.save()
            self.usuario_destino.direcciones_destino.update(is_active=True)
        
        self.direcciones_cliente_courier.update(is_active=True)
        
        return super().delete(*args, **kwargs) if kwargs.get('hard_delete', False) else None
    

    def __str__(self):
        return f"{self.nombre}, {self.apellido}"
    

class Direccion(models.Model):
    estado = models.CharField(verbose_name='Estado', max_length=150, blank=False, null=False)
    municipio = models.CharField(verbose_name='Municipio', max_length=150, blank=False, null=False)
    sector = models.CharField(verbose_name='Sector', max_length=150, blank=False, null=False)
    casa = models.CharField(verbose_name='Casa', max_length=150, blank=False, null=False)

    # Relaciones opcionales
    cliente_natural = models.ForeignKey(
        ClientNatural,
        on_delete=models.CASCADE,
        related_name="direcciones_cliente_natural",
        null=True,
        blank=True
    )
    
    cliente_courier = models.ForeignKey(
        ClientCourier,
        on_delete=models.CASCADE,
        related_name="direcciones_cliente_courier",
        null=True,
        blank=True
    )

    #--------------------------->

    cliente_quien_envia = models.ForeignKey(
        ClienteQuienEnvia,
        on_delete=models.CASCADE,
        related_name="direcciones_quien_envia",
        null=True,
        blank=True
    )

    cliente_quien_recibe = models.ForeignKey(
        ClienteQuienRecibe,
        on_delete=models.CASCADE,
        related_name="direcciones_quien_recibe",
        null=True,
        blank=True
    )

    cliente_destino = models.ForeignKey(
        ClienteUsuarioDestino,
        on_delete=models.CASCADE,
        related_name="direcciones_destino",
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default = True)
    historical = HistoricalRecords()

    def clean(self):
        if not (self.cliente_natural or self.cliente_courier):
            raise ValidationError("Debe relacionarse con al menos un tipo de cliente")
        if self.cliente_natural and self.cliente_courier:
            raise ValidationError("Solo puede relacionarse con un tipo de cliente")
        
        # si el cliente es natural deben haber direcciones para quien envia y para quien recibe
        if self.cliente_natural:
            if not (self.cliente_quien_envia or self.cliente_quien_recibe):
                raise ValidationError("los clientes quien recibe y quien envia deben tener direcciones")
        

        #si el cliente es courrier deben haber direccioens para el cliente destino tambien
        if self.cliente_courier:
            if not self.cliente_destino:
                raise ValidationError("Cliente destino debe tener direccion.")
        


    def __str__(self):
        return f"{self.casa}, {self.sector}, {self.municipio}, {self.estado}"
    

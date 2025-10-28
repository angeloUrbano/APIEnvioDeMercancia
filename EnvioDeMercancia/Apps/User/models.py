from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin , Group
from simple_history.models import HistoricalRecords




from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError




class UserManager(BaseUserManager):
    def _create_user(self, username, email, name, last_name, password, is_staff, is_superuser, groups=None, **extra_fields):
        user = self.model(
            username=username,
            email=email,
            name=name,
            last_name=last_name,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        
        # Si se proporcionan grupos, los asignamos al usuario
        if groups:
            user.groups.set(groups)
            
        return user

    def create_user(self, username, email, name, last_name, password=None, groups=None, **extra_fields):
        return self._create_user(username, email, name, last_name, password, False, False, groups, **extra_fields)

    def create_superuser(self, username, email, name, last_name, password=None, groups=None, **extra_fields):
        return self._create_user(username, email, name, last_name, password, True, True, groups, **extra_fields)

"""
segundo nombre y segundo apellido

#### se deben crear los roles de usuario pero se esta en la espera de la informacion que debe mandar el cliente #####


"""
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length = 255, unique = True)
    
    email = models.EmailField('Correo Electrónico',max_length = 255, unique = True,)
    correo_aux = models.EmailField(verbose_name='correo aux',max_length=254, unique=True , blank= True, null=True)

    name = models.CharField('Nombre', max_length = 255, blank = True, null = True)
    second_name=  models.CharField('Segundo Nombre', max_length = 255, blank = True, null = True)
    last_name = models.CharField('Apellido', max_length = 255, blank = True, null = True)
    secound_last_name = models.CharField("segundo Apellido" , max_length=100 , blank=True , null=True)
    
    identificacion = models.CharField(verbose_name='identificacion', unique=True ,max_length = 150, blank= True, null=True)
    telefono = models.CharField(max_length = 20 , blank= True, null=True , validators=[
            RegexValidator(
                regex=r'^\+?[0-9\s\-]+$',  # Permite: +, dígitos, espacios y guiones
                                message="Ingrese un número telefónico válido (ej: +1234567890 o 1234567890)")])
    telefono_aux = models.CharField(max_length = 20 , blank= True, null=True , validators=[
            RegexValidator(
                regex=r'^\+?[0-9\s\-]+$',  # Permite: +, dígitos, espacios y guiones
                                message="Ingrese un número telefónico válido (ej: +1234567890 o 1234567890)")])
    image = models.ImageField('Imagen de perfil', upload_to='perfil/', max_length=255, null=True, blank = True)
    
    codigo_cliente = models.CharField(verbose_name="codigo de cliente" , max_length=200, blank= True, null=True )
    
    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank="False",
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="custom_user_set",
        related_query_name="user" 
    )
    
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    historical = HistoricalRecords()
    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','name','last_name']

    def __str__(self):
        return f'{self.name} {self.last_name}'



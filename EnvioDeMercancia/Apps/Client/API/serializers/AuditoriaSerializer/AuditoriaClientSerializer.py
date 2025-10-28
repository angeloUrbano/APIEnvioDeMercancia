from rest_framework import serializers
#from EnvioDeMercancia.Apps.Client.models import ClienteUsuarioDestino , ClienteQuienEnvia , ClienteQuienRecibe , ClientNatural , Direccion



from EnvioDeMercancia.Apps.Client.models import ClientNatural




class ClientNaturalHistoricalSerializer(serializers.ModelSerializer):


    history_user = serializers.SerializerMethodField()
    history_type_display = serializers.SerializerMethodField()
    
    class Meta:
        model = ClientNatural.historical.model

        fields = [
            'history_id',
            'nombre',
            'segundo_nombre',
            'apellido',
            'segundo_apellido',
            'identificacion',
            'correo',
            'correo_aux',
            'telefono',
            'telefono_aux',
            'is_active',
            'history_date',
            'history_change_reason',
            'history_type',
            'history_type_display',
            'history_user'
        ]

    def get_history_user(self, obj):
      
        if obj.history_user is not None:
            return{
                "usuario":obj.history_user.username,
                "nombre": obj.history_user.name,
                "apellido":obj.history_user.last_name,
                "email":obj.history_user.email
            }   
        return None
    

    def get_history_type_display(self , obj):

        return{
            '+': 'Creación',
            '~': 'Actualización',
            '-': 'Eliminación'
        }.get(obj.history_type, obj.history_type)
    





































"""




class ClientDestinoHistoricalSerializer(serializers.ModelSerializer):

    history_user = serializers.SerializerMethodField()
    history_type_display = serializers.SerializerMethodField()
    
    class Meta:
        model = ClienteUsuarioDestino.historical.model

        fields = [
            'history_id',
            'nombre',
            'apellido',
            'identificacion',
            'correo',
            'correo_aux',
            'telefono',
            'telefono_aux',
            'is_active',
            'history_date',
            'history_change_reason',
            'history_type',
            'history_type_display',
            'history_user'
        ]

    def get_history_user(self, obj):
      
        if obj.history_user is not None:
            return{
                "usuario":obj.history_user.username,
                "nombre": obj.history_user.name,
                "apellido":obj.history_user.last_name,
                "email":obj.history_user.email
            }   
        return None
    

    def get_history_type_display(self , obj):

        return{
            '+': 'Creación',
            '~': 'Actualización',
            '-': 'Eliminación'
        }.get(obj.history_type, obj.history_type)
    



#-----------------------------------------------------

class ClienteQuienEnviaHistoricalSerializer(serializers.ModelSerializer):

    history_user = serializers.SerializerMethodField()
    history_type_display = serializers.SerializerMethodField()
    
    class Meta:
        model = ClienteQuienEnvia.historical.model

        fields = [
            'history_id',
            'nombre',
            'apellido',
            'identificacion',
            'correo',
            'correo_aux',
            'telefono',
            'telefono_aux',
            'is_active',
            'history_date',
            'history_change_reason',
            'history_type',
            'history_type_display',
            'history_user'
        ]

    def get_history_user(self, obj):
      
        if obj.history_user is not None:
            return{
                "usuario":obj.history_user.username,
                "nombre": obj.history_user.name,
                "apellido":obj.history_user.last_name,
                "email":obj.history_user.email
            }   
        return None
    

    def get_history_type_display(self , obj):

        return{
            '+': 'Creación',
            '~': 'Actualización',
            '-': 'Eliminación'
        }.get(obj.history_type, obj.history_type)
    






#-----------------------------------------------------

class ClienteQuienRecibeHistoricalSerializer(serializers.ModelSerializer):

    history_user = serializers.SerializerMethodField()
    history_type_display = serializers.SerializerMethodField()
    
    class Meta:
        model = ClienteQuienRecibe.historical.model

        fields = [
            'history_id',
            'nombre',
            'apellido',
            'identificacion',
            'correo',
            'correo_aux',
            'telefono',
            'telefono_aux',
            'is_active',
            'history_date',
            'history_change_reason',
            'history_type',
            'history_type_display',
            'history_user'
        ]

    def get_history_user(self, obj):
      
        if obj.history_user is not None:
            return{
                "usuario":obj.history_user.username,
                "nombre": obj.history_user.name,
                "apellido":obj.history_user.last_name,
                "email":obj.history_user.email
            }   
        return None
    

    def get_history_type_display(self , obj):

        return{
            '+': 'Creación',
            '~': 'Actualización',
            '-': 'Eliminación'
        }.get(obj.history_type, obj.history_type)
    



#---------------------------------------------------------------

class ClientNaturalHistoricalSerializer(serializers.ModelSerializer):


    history_user = serializers.SerializerMethodField()
    history_type_display = serializers.SerializerMethodField()
    
    class Meta:
        model = ClientNatural.historical.model

        fields = [
            'history_id',
            'nombre',
            'apellido',
            'identificacion',
            'correo',
            'correo_aux',
            'telefono',
            'telefono_aux',
            'is_active',
            'history_date',
            'history_change_reason',
            'history_type',
            'history_type_display',
            'history_user'
        ]

    def get_history_user(self, obj):
      
        if obj.history_user is not None:
            return{
                "usuario":obj.history_user.username,
                "nombre": obj.history_user.name,
                "apellido":obj.history_user.last_name,
                "email":obj.history_user.email
            }   
        return None
    

    def get_history_type_display(self , obj):

        return{
            '+': 'Creación',
            '~': 'Actualización',
            '-': 'Eliminación'
        }.get(obj.history_type, obj.history_type)
    




#---------------------------------------------------------------

class ClientCourierHistoricalSerializer(serializers.ModelSerializer):


    history_user = serializers.SerializerMethodField()
    history_type_display = serializers.SerializerMethodField()
    
    class Meta:
        model = ClientNatural.historical.model

        fields = [
            'history_id',
            'nombre',
            'apellido',
            'identificacion',
            'correo',
            'correo_aux',
            'telefono',
            'telefono_aux',
            'is_active',
            'history_date',
            'history_change_reason',
            'history_type',
            'history_type_display',
            'history_user'
        ]

    def get_history_user(self, obj):
      
        if obj.history_user is not None:
            return{
                "usuario":obj.history_user.username,
                "nombre": obj.history_user.name,
                "apellido":obj.history_user.last_name,
                "email":obj.history_user.email
            }   
        return None
    

    def get_history_type_display(self , obj):

        return{
            '+': 'Creación',
            '~': 'Actualización',
            '-': 'Eliminación'
        }.get(obj.history_type, obj.history_type)
    



#---------------------------------------------------------------

class DireccionHistoricalSerializer(serializers.ModelSerializer):



    history_user = serializers.SerializerMethodField()
    history_type_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Direccion.historical.model

        fields = [

            'history_id',
            'estado',
            'municipio',
            'sector',
            'casa',
            'cliente_natural',
            'cliente_courier',
            'cliente_quien_envia',
            'cliente_quien_recibe',
            'cliente_destino',
            'is_active',
            'history_date',
            'history_change_reason',
            'history_type',
            'history_type_display',
            'history_user'
        ]

    def get_history_user(self, obj):
      
        if obj.history_user is not None:
            return{
                "usuario":obj.history_user.username,
                "nombre": obj.history_user.name,
                "apellido":obj.history_user.last_name,
                "email":obj.history_user.email
            }   
        return None
    

    def get_history_type_display(self , obj):

        return{
            '+': 'Creación',
            '~': 'Actualización',
            '-': 'Eliminación'
        }.get(obj.history_type, obj.history_type)




"""
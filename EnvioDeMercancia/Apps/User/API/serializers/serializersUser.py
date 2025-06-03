from rest_framework import serializers


from EnvioDeMercancia.Apps.User.models import User

class userSerilizer(serializers.ModelSerializer):

    class Meta:
        model= User 
        fields = ["username" , "email" , "name" , "last_name" , "password" ]

    #that function let me encriptar the password and save the all information
    def create (self , validate_data):
        user = User(**validate_data)
        user.set_password(validate_data["password"]) 
        user.save()

        return user
    

    def update(self  , instance , validate_data):
        update_user = super().update(instance , validate_data)
        update_user.set_password(validate_data["password"])
        update_user.save()
        return update_user

    def to_representation(self, instance):
        return{
            "id":instance.id,
            "username": instance.username,
            "name": instance.name,
            "last_name": instance.last_name,
            "email": instance.email,
            "password":instance.password
        }
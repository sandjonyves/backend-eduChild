from .models import Child
from rest_framework import serializers



class ChildSerializers(serializers.ModelSerializer):

    class Meta:
        model =Child
        fields =('__all__')
    
    def update(self,instance,validated_data):
        print ('This here')
        update_instace = Child.objects.get(pk=instance.id)
        Child.objects.filter(pk=instance.id)\
                            .update(**validated_data)
    
        return update_instace
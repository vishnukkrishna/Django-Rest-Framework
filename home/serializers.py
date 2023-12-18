from rest_framework import serializers
from .models import Person, Color


class LoginSerializer(serializers.Serializer):

  email    = serializers.EmailField()
  password = serializers.CharField(max_length=250)


class ColorSerializer(serializers.ModelSerializer):

  class Meta:
    model  = Color
    fields = ['id', 'color_name']

class PeopleSerializer(serializers.ModelSerializer):

  color      = ColorSerializer()
  color_info = serializers.SerializerMethodField()

  class Meta:
    model  = Person
    fields = '__all__'
    # depth  = 1

  def get_color_info(self, obj):
    color_obj = Color.objects.get(id = obj.color.id)
    return {'color': color_obj.color_name, 'hex_code': '#000'}

  def validate(self, data):
    special_characters = "!@#$%^&*()_+-=,<>/"
    if any(c in special_characters for c in data['name']):
      raise serializers.ValidationError('Name cannot contain special characters')

    if data['age'] < 18:
      raise serializers.ValidationError('Age should be grater than 18')
    return data
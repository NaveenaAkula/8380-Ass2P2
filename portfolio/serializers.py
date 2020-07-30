from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
            model = Customer
            fields = ('name', 'address', 'cust_number', 'city', 'state', 'zipcode', 'email', 'email', 'cell_phone')

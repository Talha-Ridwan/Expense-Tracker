from rest_framework import serializers
from mainapp.models import User,UserExpense

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only = True)
    class Meta:
        model = User
        fields = ['email','name','password','password2','tc','number']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email','password']

class UserProfileSeializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','name','number']


class UserExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExpense
        fields = ['id', 'expense_type', 'amount', 'description', 'date', 'created_at']
        read_only_fields = ['created_at']

class QuickAddExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExpense
        fields = ['amount', 'description']

    def create(self, validated_data):
        user = self.context['request'].user
        return UserExpense.objects.create(user=user, expense_type='others', **validated_data)
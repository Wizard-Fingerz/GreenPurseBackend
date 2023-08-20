from rest_framework import serializers
from .models import Transaction
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.email = validated_data.get("email", instance.email)
        instance.age = validated_data.get("age", instance.age)
        instance.updated_at = validated_data.get("updated_at", instance.updated_at)
        instance.save()
        return instance


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.account = validated_data.get("account", instance.account)
        instance.amount = validated_data.get("amount", instance.amount)
        instance.type = validated_data.get("type", instance.type)
        instance.category = validated_data.get("category", instance.category)
        instance.save()
        return instance


class SummaryByAccountSerializer(serializers.Serializer):
    account = serializers.CharField(max_length=15)
    total_inflow = serializers.DecimalField(decimal_places=2, max_digits=30)
    total_outflow = serializers.DecimalField(decimal_places=2, max_digits=30)
    balance = serializers.DecimalField(decimal_places=2, max_digits=30)


class SummaryByCategorySerializer(serializers.Serializer):
    inflow = serializers.DictField(
        child=serializers.DecimalField(decimal_places=2, max_digits=30)
    )
    outflow = serializers.DictField(
        child=serializers.DecimalField(decimal_places=2, max_digits=30)
    )
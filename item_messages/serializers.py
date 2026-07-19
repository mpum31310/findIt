from rest_framework import serializers
from .models import Message
from items.serializers import ItemSerializer


class MessageSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    item_qr_data = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Message
        fields = ('id', 'item', 'item_qr_data', 'sender_name', 'sender_email', 
                  'sender_phone', 'message', 'is_read', 'created_at')
        read_only_fields = ('id', 'is_read', 'created_at')

    def create(self, validated_data):
        qr_data = validated_data.pop('item_qr_data', None)
        if qr_data:
            from items.models import Item
            try:
                item = Item.objects.get(qr_code_data=qr_data)
                validated_data['item'] = item
            except Item.DoesNotExist:
                raise serializers.ValidationError({'item_qr_data': 'Invalid QR code'})
        
        return super().create(validated_data)


class MessageCreateSerializer(serializers.ModelSerializer):
    """Public serializer for creating messages (no authentication required)"""
    item_qr_data = serializers.CharField(required=True)

    class Meta:
        model = Message
        fields = ('item_qr_data', 'sender_name', 'sender_email', 'sender_phone', 'message')

    def create(self, validated_data):
        qr_data = validated_data.pop('item_qr_data')
        from items.models import Item
        try:
            item = Item.objects.get(qr_code_data=qr_data)
            validated_data['item'] = item
            return super().create(validated_data)
        except Item.DoesNotExist:
            raise serializers.ValidationError({'item_qr_data': 'Invalid QR code'})


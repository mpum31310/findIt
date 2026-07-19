from rest_framework import serializers
from .models import Item
from children.serializers import ChildSerializer


class ItemSerializer(serializers.ModelSerializer):
    child = ChildSerializer(read_only=True)
    child_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    qr_code_url = serializers.SerializerMethodField()
    item_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'child', 'child_id', 'qr_code', 
                  'qr_code_url', 'qr_code_data', 'item_image', 'item_image_url', 
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'qr_code', 'qr_code_data', 'created_at', 'updated_at')

    def get_qr_code_url(self, obj):
        if obj.qr_code:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.qr_code.url)
            return obj.qr_code.url
        return None

    def get_item_image_url(self, obj):
        if obj.item_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.item_image.url)
            return obj.item_image.url
        return None

    def create(self, validated_data):
        child_id = validated_data.pop('child_id', None)
        validated_data['parent'] = self.context['request'].user
        if child_id:
            from children.models import Child
            try:
                child = Child.objects.get(id=child_id, parent=validated_data['parent'])
                validated_data['child'] = child
            except Child.DoesNotExist:
                pass
        
        item = Item.objects.create(**validated_data)
        item.generate_qr_code()
        item.save()
        return item

    def update(self, instance, validated_data):
        child_id = validated_data.pop('child_id', None)
        if child_id is not None:
            from children.models import Child
            try:
                child = Child.objects.get(id=child_id, parent=instance.parent)
                instance.child = child
            except Child.DoesNotExist:
                instance.child = None
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


from rest_framework import serializers

from shop.products.models import Product, Status, Image


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['availibility']


class ProductSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField('get_status')
    image = serializers.SerializerMethodField('get_image')

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'sku', 'status', 'image'
        ]

    def get_status(self, obj):
        return obj.status.availibility

    def get_image(self, obj):
        return {
            "path": obj.image.image.url,
            "formats": [obj.image.get_format(), 'webp']
        } if obj.image else {"path": None, "formats": None}


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image', )

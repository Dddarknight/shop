from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404

from shop.products.models import Product, Image
from shop.products.serializers import ImageSerializer, ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status__availibility=status)
        sku = self.request.query_params.get('sku')
        if sku:
            queryset = queryset.filter(sku=sku)
        title = self.request.query_params.get('title')
        if title:
            queryset = queryset.filter(title=title)
        return queryset


class ImageUploadView(ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        file = request.FILES['image']
        image = Image.objects.create(
            image=file
        )
        product = get_object_or_404(Product, pk=pk)
        product.image = image
        product.save()
        image.save_to_webp()
        return Response(status=200)

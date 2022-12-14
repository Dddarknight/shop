from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image as PillowImage


class Status(models.Model):
    class Meta:
        verbose_name = _('status')
        verbose_name_plural = _('statuses')

        ordering = ['availibility']

    class Availibility(models.TextChoices):
        IN_STOCK = 'in-stock', _('in-stock')
        PREORDER = 'preorder', _('preorder')
        COMING_SOON = 'coming-soon', _('coming-soon')
        OUT_OF_STOCK = 'out-of-stock', _('out-of-stock')
        OUT_OF_PRODUCTION = 'out-of-production', _('out-of-production')

    availibility = models.CharField(
        _('availibility'),
        max_length=20,
        choices=Availibility.choices,
        unique=True,
    )
    slug = models.SlugField(_('slug'), max_length=255)

    def __str__(self):
        return self.availibility


class Image(models.Model):

    image = models.ImageField(upload_to='images')

    def save_to_webp(self):
        image = PillowImage.open(self.image.path).convert("RGB")
        image_name = '.'.join(self.image.path.split('.')[:-1])
        image.save(f'{image_name}.webp', 'webp')

    def get_format(self):
        image = PillowImage.open(self.image.path)
        return image.format.lower()


class Product(models.Model):
    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

        ordering = ['title']

    title = models.CharField(_('title'), max_length=255)
    sku = models.CharField(_('sku'), max_length=255, unique=True)
    slug = models.SlugField(_('slug'), max_length=255)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    image = models.OneToOneField(Image, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


class PropertyObject(models.Model):
    class Meta:
        verbose_name = _('property object')
        verbose_name_plural = _('properties objects')

        ordering = ['title']

    class Type(models.TextChoices):
        STRING = 'string', _('string')
        DECIMAL = 'decimal', _('decimal')

    title = models.CharField(_('title'), max_length=255)
    code = models.SlugField(_('code'), max_length=255)
    value_type = models.CharField(
        _('value type'), max_length=10, choices=Type.choices
    )

    def __str__(self):
        return f'{self.title}'


class Value(models.Model):
    class Meta:
        verbose_name = _('value')
        verbose_name_plural = _('values')

        ordering = ['value_string', 'value_decimal']

    property_object = models.ForeignKey(
        to=PropertyObject, on_delete=models.PROTECT
    )

    value_string = models.CharField(
        _('value string'), max_length=255, blank=True, null=True
    )
    value_decimal = models.DecimalField(
        _('value decimal'),
        max_digits=11,
        decimal_places=2,
        blank=True,
        null=True,
    )
    code = models.SlugField(_('code'), max_length=255)

    products = models.ManyToManyField(to=Product)

    def __str__(self):
        return str(
            getattr(self, f'value_{self.property_object.value_type}', None)
        )

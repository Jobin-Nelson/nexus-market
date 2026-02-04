from enum import unique
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.


class User(AbstractUser):
    age = models.IntegerField(blank=True, null=True)


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='vendors/images', blank=True, null=True)

    def __str__(self):
        return self.name


class Category(MPTTModel):
    name = models.CharField(max_length=255, unique=True)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name='children'
    )
    description = models.TextField(null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class ProductSpec(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products/images', blank=True, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField("Created at", auto_now_add=True, editable=False)
    updated_at = models.DateTimeField("Updated at", auto_now=True)
    slug = models.SlugField(max_length=255, blank=True, editable=False)

    class Meta:
        abstract = True
        ordering = ['-created_at']
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            model_class = self.__class__
            while model_class.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class PhysicalProduct(ProductSpec):
    dimensions = models.CharField(max_length=100, blank=True, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['slug', 'category'], name='unique_physicalproduct_slug_per_category')
        ]

class DigitalProduct(ProductSpec):
    os = models.CharField(max_length=100, blank=True, null=True)
    requirements = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['slug', 'category'], name='unique_digitalproduct_slug_per_category')
        ]


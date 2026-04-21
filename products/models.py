from uuid import uuid4
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def custom_name(instance, filename):
    ext = filename.split('.')[-1]
    return f'products/{uuid4().hex}.{ext}'


class Product(models.Model):
    name = models.CharField(max_length=64, null=False)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=custom_name, null=True, blank=True)
    stock = models.PositiveSmallIntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

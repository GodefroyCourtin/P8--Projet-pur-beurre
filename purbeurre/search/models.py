from django.db import models
class products(models.Model):
    id = models.BigIntegerField(primary_key=True)
    categorie = models.CharField(max_length=40)
    nom = models.CharField(max_length=200)
    description = models.TextField()
    indice = models.CharField(max_length=10)
    date_update = models.CharField(max_length=200)
    url = models.TextField()

class categories(models.Model):
    name = models.CharField(max_length=200)
    product = models.ManyToManyField(products)
    class Meta:
        ordering = ('name',)
    def __str__(self):
        return self.name

class ingredients(models.Model):
    name = models.CharField(max_length=200)
    product = models.ManyToManyField(products)
    class Meta:
        ordering = ('name',)
    def __str__(self):
        return self.name

class product_save(models.Model):
    id_product = models.ManyToManyField(products)
    id_save_product = models.ManyToManyField(products, related_name="product_replace")

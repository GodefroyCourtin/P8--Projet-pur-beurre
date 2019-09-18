from django.db import models

class Main_categorie(models.Model):
    name = models.CharField(max_length=60)
    class Meta:
        ordering = ('name',)
    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.BigIntegerField(primary_key=True)
    categorie = models.ForeignKey(Main_categorie, on_delete=models.CASCADE)
    nom = models.CharField(max_length=200)
    description = models.TextField()
    indice = models.CharField(max_length=10)
    date_update = models.CharField(max_length=200)
    url = models.TextField()

class Sub_categorie(models.Model):
    name = models.CharField(max_length=200)
    product = models.ManyToManyField(Product)
    class Meta:
        ordering = ('name',)
    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    product = models.ManyToManyField(Product)
    class Meta:
        ordering = ('name',)
    def __str__(self):
        return self.name

# class product_save(models.Model):
#     id_product = models.ManyToManyField(Product)
#     id_save_product = models.ManyToManyField(Product, related_name="product_replace")

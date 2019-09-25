from django.db import models

class Main_categorie(models.Model):
    name = models.CharField(max_length=60)
    class Meta:
        ordering = ('name',)
    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.BigIntegerField(primary_key=True)
    main_categorie = models.ForeignKey(Main_categorie, on_delete=models.CASCADE)
    nom = models.CharField(max_length=200)
    description = models.TextField()
    indice = models.CharField(max_length=10)
    date_update = models.CharField(max_length=200)
    url = models.TextField()

    def compare_search(self):
        list_sub_cat_product = [str(i.id) for i in self.sub_categorie_set.all()]
        list_ingredient_product = [str(i.id) for i in self.ingredient_set.all()]
        dict_compare = self.sub_cat(list_sub_cat_product)
        dict_compare = self.ing(list_ingredient_product, dict_compare)
    
        if len(dict_compare) > 5:
            dict_compare = sorted(dict_compare.items(),key = lambda x : x[1], reverse=True)[:5]
        else:
            dict_compare = sorted(dict_compare.items(),key = lambda x : x[1], reverse=True)

        return {"products" : [Product.objects.filter(id=id_product[0]) for id_product in dict_compare] }
    
    def ing(self, list_ingredient_product, dict_compare):
        for ing in list_ingredient_product:
            recuperate_prod = [str(i.id) for i in Product.objects.filter(ingredient__id=ing).filter(main_categorie_id=self.main_categorie_id).filter(indice__lt=self.indice)]
            for ingredient in recuperate_prod:
                if ingredient in dict_compare:
                    data = dict_compare[ingredient]
                    data += 1
                    dict_compare[ingredient] = data
                elif ingredient not in dict_compare:
                    dict_compare[ingredient] = 1
        return dict_compare

    def sub_cat(self, list_sub_cat_product):
        dict_compare = {}
        for sub_cat in list_sub_cat_product:
            recuperate_prod = [str(i.id) for i in Product.objects.filter(sub_categorie__id=sub_cat).filter(main_categorie_id=self.main_categorie_id).filter(indice__lt=self.indice)]
            for prod in recuperate_prod:
                if prod in dict_compare:
                    data = dict_compare[prod]
                    data += 1
                    dict_compare[prod] = data
                elif prod not in dict_compare:
                    dict_compare[prod] = 1
        return dict_compare

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

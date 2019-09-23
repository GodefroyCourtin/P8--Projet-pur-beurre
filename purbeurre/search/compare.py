from .models import Product, Main_categorie, Sub_categorie, Ingredient

class compare:
    def __init__(self, detail_product):
        self.detail_product = detail_product
        self.main_cat = self.detail_product.main_categorie_id
        self.indice = self.detail_product.indice
        self.sub_cat_product = [str(i.id) for i in self.detail_product.sub_categorie_set.all()]
        self.ingredient_product = [str(i.id) for i in self.detail_product.ingredient_set.all()]
        self.dict_compare = {}
        self.sub_cat()
        self.ing()
        self.dict_compare = sorted(self.dict_compare.items(),key = lambda x : x[1], reverse=True)[:5]


    def sub_cat(self):
        for sub_cat in self.sub_cat_product:
            recuperate_prod = [str(i.id) for i in Product.objects.filter(sub_categorie__id=sub_cat).filter(main_categorie_id=self.main_cat).filter(indice__lt=self.indice)]
            for prod in recuperate_prod:
                if prod in self.dict_compare:
                    data = self.dict_compare[prod]
                    data += 1
                    self.dict_compare[prod] = data
                elif prod not in self.dict_compare:
                    self.dict_compare[prod] = 1

    def ing(self):
        for ing in self.ingredient_product:
            recuperate_prod = [str(i.id) for i in Product.objects.filter(ingredient__id=ing).filter(main_categorie_id=self.main_cat).filter(indice__lt=self.indice)]
            for ingredient in recuperate_prod:
                if ingredient in self.dict_compare:
                    data = self.dict_compare[ingredient]
                    data += 1
                    self.dict_compare[ingredient] = data
                elif ingredient not in self.dict_compare:
                    self.dict_compare[ingredient] = 1

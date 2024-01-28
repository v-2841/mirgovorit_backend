from django.contrib import admin
from django.contrib.auth.models import Group

from recipes.models import Product, Recipe, RecipeProduct


class RecipeProductInline(admin.TabularInline):
    model = RecipeProduct
    min_num = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeProductInline]


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'cooked')


class RecipeProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'recipe', 'weight')


admin.site.register(Product, ProductAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeProduct, RecipeProductAdmin)

admin.site.unregister(Group)

from django.urls import path

from recipes import views


app_name = 'recipes'
urlpatterns = [
    path('add_product_to_recipe/', views.add_product_to_recipe,
         name='add_product_to_recipe'),
    path('cook_recipe/', views.cook_recipe, name='cook_recipe'),
    path('show_recipes_without_product/', views.show_recipes_without_product,
         name='show_recipes_without_product'),
]

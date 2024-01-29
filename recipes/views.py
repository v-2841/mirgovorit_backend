from django.db import transaction
from django.db.models import F, Q, prefetch_related_objects
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods

from recipes.models import Product, Recipe, RecipeProduct


@require_http_methods(['GET'])
def add_product_to_recipe(request):
    product_id = request.GET.get('product_id', '')
    recipe_id = request.GET.get('recipe_id', '')
    weight = request.GET.get('weight', '')
    if not (product_id and recipe_id and weight):
        return HttpResponse(status=400)
    product = get_object_or_404(Product, pk=product_id)
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe_product, created = RecipeProduct.objects.get_or_create(
        product=product, recipe=recipe, defaults={'weight': weight}
    )
    if not created:
        recipe_product.weight = weight
        recipe_product.save()
    return HttpResponse(status=200)


@require_http_methods(['GET'])
@transaction.atomic
def cook_recipe(request):
    recipe_id = request.GET.get('recipe_id', '')
    if not recipe_id:
        return HttpResponse(status=400)
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    prefetch_related_objects([recipe], 'products')
    Product.objects.filter(
        id__in=recipe.products.values_list('id')).update(
            cooked=F('cooked') + 1)
    return HttpResponse(status=200)


@require_http_methods(['GET'])
def show_recipes_without_product(request):
    product_id = request.GET.get('product_id', '')
    if not product_id:
        return HttpResponse(status=400)
    product = get_object_or_404(Product, pk=product_id)
    recipes = Recipe.objects.filter(~Q(recipeproduct__product=product) | (Q(
        recipeproduct__product=product) & Q(
            recipeproduct__weight__lt=10))).distinct().order_by('id')
    context = {'recipes': recipes}
    return render(request,
                  'recipes/show_recipes_without_product.html', context)

from django.test import TestCase, Client
from django.urls import reverse
from recipes.models import Product, Recipe, RecipeProduct


class RecipeAppTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(name='Product')
        self.recipe1 = Recipe.objects.create(name='Recipe1')
        self.recipe2 = Recipe.objects.create(name='Recipe2')
        self.recipe3 = Recipe.objects.create(name='Recipe3')

    def test_add_product_to_recipe(self):
        url = reverse('recipes:add_product_to_recipe')
        data = {'product_id': self.product.id,
                'recipe_id': self.recipe1.id, 'weight': 100}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(RecipeProduct.objects.filter(
            product=self.product, recipe=self.recipe1, weight=100).exists())
        data = {'product_id': self.product.id,
                'recipe_id': self.recipe1.id, 'weight': 50}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(RecipeProduct.objects.filter(
            product=self.product, recipe=self.recipe1, weight=50).exists())

    def test_cook_recipe(self):
        RecipeProduct.objects.create(
            product=self.product, recipe=self.recipe1, weight=100)
        url = reverse('recipes:cook_recipe')
        data = {'recipe_id': self.recipe1.id}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.get(id=self.product.id).cooked, 1)

    def test_show_recipes_without_product(self):
        RecipeProduct.objects.create(
            product=self.product, recipe=self.recipe1, weight=100)
        RecipeProduct.objects.create(
            product=self.product, recipe=self.recipe2, weight=5)
        url = reverse('recipes:show_recipes_without_product')
        data = {'product_id': self.product.id}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.recipe1 in response.context['recipes'])
        self.assertTrue(self.recipe2 in response.context['recipes'])
        self.assertTrue(self.recipe3 in response.context['recipes'])

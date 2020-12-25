from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientTestApi(TestCase):
    """Test publicly available ingredient"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test user authentication is required"""

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientTestApi(TestCase):
    """Test private ingredient api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """Test retrieving a list of ingredients"""
        Ingredient.objects.create(
            user=self.user,
            name='Cucumber'
        )
        Ingredient.objects.create(
            user=self.user,
            name='tomatos'
        )
        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertTrue(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_objects_of_user(self):
        """Test retrieving ingredient that only authenticated user"""
        user2 = get_user_model().objects.create_user(
            'user2@gmail.com',
            'test2pass'
        )
        Ingredient.objects.create(user=user2, name='Cheese')
        ingredient = Ingredient.objects.create(user=self.user, name='milk')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_successful(self):
        """Test an ingredient create successful"""
        payload = {
            'name': 'Kale'
        }
        res = self.client.post(INGREDIENTS_URL, payload)
        ingredient = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(ingredient)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_ingredient_fail(self):
        """Test create an ingredient with invalid data"""
        payload = {
            'name': ''
        }
        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

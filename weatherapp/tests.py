from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse
from .params import wind_direction, wind_convert


class IndexViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('index')

    def test_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_valid_city(self):
        response = self.client.post(self.url, {'city': 'Moscow'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Температура')

    def test_invalid_city(self):
        response = self.client.post(self.url, {'city': 'InvalidCityName12345'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Город не найден')




class UtilsTests(SimpleTestCase):
    def test_wind_direction(self):
        self.assertEqual(wind_direction(0), 'Север')
        self.assertEqual(wind_direction(11.25), 'Северо-восток')
        self.assertEqual(wind_direction(258.75), 'Запад')

    def test_wind_convert(self):
        self.assertEqual(wind_convert(1), 0.28)
        self.assertEqual(wind_convert(36), 10.00)
        self.assertEqual(wind_convert(3.6), 1.00)

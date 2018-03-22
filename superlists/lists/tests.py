from django.http import HttpRequest
from django.shortcuts import render
from django.template.loader import render_to_string
from django.test import TestCase

from django.urls import resolve
from lists.views import home_page


class HomePageTest(TestCase):
    def test_root_rul_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_caan_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': '신규 작업 아이템'})
        self.assertIn('신규 작업 아이템', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')

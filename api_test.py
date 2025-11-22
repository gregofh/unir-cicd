import http.client
import os
import unittest
from urllib.request import urlopen
import urllib.error
from unittest.mock import patch
import pytest

def mocked_validation(*args, **kwargs):
    return True
    
BASE_URL = os.environ.get("BASE_URL")
DEFAULT_TIMEOUT = 2  # in secs


@pytest.mark.api
class TestApi(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(BASE_URL, "URL no configurada")
        self.assertTrue(len(BASE_URL) > 8, "URL no configurada")

    def test_api_add(self):
        url = f"{BASE_URL}/calc/add/2/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(response.status, http.client.OK, f"Error en la petición API a {url}")
        body = response.read().decode('utf-8')
        self.assertEqual(body, "4")

    def test_api_substract(self):
        url = f"{BASE_URL}/calc/substract/2/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(response.status, http.client.OK, f"Error en la petición API a {url}")
    
    @patch('app.util.validate_permissions', side_effect=mocked_validation, create=True)
    def test_api_multiply(self, _validate_permissions):
        url = f"{BASE_URL}/calc/multiply/2/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(response.status, http.client.OK, f"Error en la petición API a {url}")
        body = response.read().decode('utf-8')
        self.assertEqual(body, "4")
        
    def test_api_divide(self):
        url = f"{BASE_URL}/calc/divide/2/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(response.status, http.client.OK, f"Error en la petición API a {url}")
        
    def test_api_power(self):
        url = f"{BASE_URL}/calc/power/2/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(response.status, http.client.OK, f"Error en la petición API a {url}")

    def test_api_sqrt(self):
        url = f"{BASE_URL}/calc/sqrt/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(response.status, http.client.OK, f"Error en la petición API a {url}")

    # Ahora vamos a comtemplar los errores
    def test_api_add_invalid_type_fails(self):
        url = f"{BASE_URL}/calc/add/dos/2"
        with self.assertRaises(urllib.error.HTTPError) as e:
            urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(e.exception.code, http.client.BAD_REQUEST)

    def test_api_divide_by_zero_fails(self):
        url = f"{BASE_URL}/calc/divide/10/0"
        with self.assertRaises(urllib.error.HTTPError) as e:
            urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(e.exception.code, http.client.BAD_REQUEST)
    
    def test_api_sqrt_negative_fails(self):
        url = f"{BASE_URL}/calc/sqrt/-25"
        with self.assertRaises(urllib.error.HTTPError) as e:
            urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(e.exception.code, http.client.BAD_REQUEST)

    def test_api_log10_zero_fails(self):
        url = f"{BASE_URL}/calc/log10/0"
        with self.assertRaises(urllib.error.HTTPError) as e:
            urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(e.exception.code, http.client.BAD_REQUEST)

    def test_api_log10_negative_fails(self):
        url = f"{BASE_URL}/calc/log10/-100"
        with self.assertRaises(urllib.error.HTTPError) as e:
            urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(e.exception.code, http.client.BAD_REQUEST)


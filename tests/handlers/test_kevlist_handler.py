from unittest import TestCase
from unittest.mock import patch

from src.handlers.kevlist_handler import KevListHandler

class TestKevListHandler(TestCase):

  @patch('urllib.request.urlopen')
  @patch('json.loads')
  def test_load_json(self, loads, urlopen):

    kev_list = KevListHandler('https://my/asome/url/')
    kev_list.load_json()

    urlopen.assert_called_with('https://my/asome/url/')
    urlopen.return_value.read.assert_called_with()

    loads.assert_called_with(urlopen.return_value.read.return_value)
    self.assertEqual(kev_list.__dict__['_KevListHandler__data'], loads.return_value)

  def test_exists(self):
    kev_list = KevListHandler('https://my/asome/url/')
    kev_list.__dict__['_KevListHandler__data'] = {'vulnerabilities': [{'cveID': 'right_id'}]}

    right = kev_list.exists('right_id')
    wrong = kev_list.exists('wrong_id')

    self.assertTrue(right)
    self.assertFalse(wrong)



    
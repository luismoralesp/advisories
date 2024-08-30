from unittest import TestCase
from unittest.mock import patch

class TestKevListHandler(TestCase):

  @classmethod
  def setUpClass(cls):
    cls.urlopen = patch('urllib.request.urlopen').start()
  
  def tearDown(self):
    patch.stopall()

  @patch('json.loads')
  def test_load_json(self, loads):
    
    from src.handlers.KevListHandler import KevListHandler

    kev_list = KevListHandler('https://my/asome/url/')
    kev_list.load_json()

    self.urlopen.assert_called_with('https://my/asome/url/')
    self.urlopen.return_value.read.assert_called_with()

    loads.assert_called_with(self.urlopen.return_value.read.return_value)
    self.assertEqual(kev_list.__dict__['_KevListHandler__data'], loads.return_value)

  def test_exists(self):
    from src.handlers.KevListHandler import KevListHandler

    kev_list = KevListHandler('https://my/asome/url/')
    kev_list.__dict__['_KevListHandler__data'] = {'vulnerabilities': [{'cveID': 'right_id'}]}

    right = kev_list.exists('right_id')
    wrong = kev_list.exists('wrong_id')

    self.assertTrue(right)
    self.assertFalse(wrong)



    
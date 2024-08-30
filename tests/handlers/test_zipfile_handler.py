from unittest import TestCase
from unittest.mock import patch

from src.handlers.zipfile_handler import ZipFileHandler

class TestZipFileHandler(TestCase):

  @patch('zipfile.ZipFile')
  def test_append(self, ZipFile):
    zip_file = ZipFileHandler('/my/asome/zip/file')

    zip_file.append('my_asome_file1', '/my/asome/file/path')
    ZipFile.assert_called_with('/my/asome/zip/file', 'w')
    ZipFile.return_value.write.assert_called_with('/my/asome/file/path', arcname='my_asome_file1')
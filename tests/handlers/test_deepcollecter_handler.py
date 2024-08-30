from unittest import TestCase
from unittest.mock import patch, Mock, call
import os

from src.handlers.deepcollecter_handler import DeepCollecterHandler

class MockedListDir:

  mocked_folder_data = {
    '/my/asome/folder': (
      'folder1', 
      'folder2', 
      'file1'
    ),
    os.path.join('/my/asome/folder', 'folder1'): (
      'file2', 
    ), 
    os.path.join('/my/asome/folder', 'folder2'): (
      'file3', 
    ), 
  }

  def __call__(self, folder) -> list:
    return self.mocked_folder_data[folder]
  
class MockedIsFile:
  mocked_isfile_data = (
    os.path.join('/my/asome/folder', 'file1'),
    os.path.join('/my/asome/folder', 'folder1', 'file2'),
    os.path.join('/my/asome/folder', 'folder2', 'file3'),
  )

  def __call__(self, file) -> bool:
    return file in self.mocked_isfile_data

class TestDeepCollectHandler(TestCase):

  @patch('os.listdir', new_callable=MockedListDir)
  @patch('os.path.isfile', new_callable=MockedIsFile)
  def test___collect(self, listdir, isfile):

    deep_collecter = DeepCollecterHandler("/my/asome/folder")

    def my_func(file_name, file_path):
      pass

    mocked_my_func = Mock(my_func)

    deep_collecter.collect(mocked_my_func)

    mocked_my_func.assert_has_calls([
      call('file2', os.path.join('/my/asome/folder', 'folder1', 'file2')),
      call('file3', os.path.join('/my/asome/folder', 'folder2', 'file3')),
      call('file1', os.path.join('/my/asome/folder', 'file1')),
    ])
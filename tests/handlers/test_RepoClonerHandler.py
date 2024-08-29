from unittest import TestCase
from unittest.mock import patch


class TestRepoClonerHandler(TestCase):

  @classmethod
  def setUpClass(cls):
    cls.Repo = patch('git.Repo').start()
  
  def tearDown(self):
    patch.stopall()
  
  def test_clone(self):
    from src.handlers.RepoClonerHandler import RepoClonerHandler

    repo_cloner = RepoClonerHandler("my_asome_repo", "/my/asome/folder")
    repo_cloner.clone('<progress_value>')

    self.Repo.clone_from.assert_called_with("my_asome_repo", "/my/asome/folder", '<progress_value>')

  def test_pull(self):

    from src.handlers.RepoClonerHandler import RepoClonerHandler

    repo_cloner = RepoClonerHandler("my_asome_repo", "/my/asome/folder")
    repo_cloner.pull()

    self.Repo.assert_called_with("/my/asome/folder")
  


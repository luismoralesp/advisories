from unittest import TestCase
from unittest.mock import patch, Mock

from src.handlers.repocloner_handler import RepoClonerHandler

class TestRepoClonerHandler(TestCase):

  @patch('git.Repo')
  def test_clone(self, Repo):
    repo_cloner = RepoClonerHandler("my_asome_repo", "/my/asome/folder")
    repo_cloner.clone('<progress_value>')

    Repo.clone_from.assert_called_with("my_asome_repo", "/my/asome/folder", '<progress_value>')

  @patch('git.Repo')
  def test_pull(self, Repo):
    repo_cloner = RepoClonerHandler("my_asome_repo", "/my/asome/folder")
    repo_cloner.pull()

    Repo.assert_called_with("/my/asome/folder")
  
  @patch('os.path.exists')
  def test_clone_or_pull(self, exists):
    repo_cloner = RepoClonerHandler("my_asome_repo", "/my/asome/folder")
    repo_cloner.clone = Mock()
    repo_cloner.pull = Mock()

    exists.return_value = True
    repo_cloner.clone_or_pull('<progress_value>')

    repo_cloner.pull.assert_called_with()

    exists.return_value = False
    repo_cloner.clone_or_pull('<progress_value>')

    repo_cloner.clone.assert_called_with('<progress_value>')

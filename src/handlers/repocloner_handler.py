import git
import os

"""
RepoClonerHandler class
"""
class RepoClonerHandler:
  def __init__(self, repository, target_folder) -> None:
    self.__repository = repository
    self.__target_folder = target_folder

  def clone(self, progress) -> None:
    git.Repo.clone_from(self.__repository, self.__target_folder, progress)
    
  def pull(self) -> None:
    repo = git.Repo(self.__target_folder)
    origin = repo.remotes.origin
    origin.pull()

  def clone_or_pull(self, progress) -> None:
    if not os.path.exists(self.__target_folder):
      self.clone(progress)
    else:
      self.pull()

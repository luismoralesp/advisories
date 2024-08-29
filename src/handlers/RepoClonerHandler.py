from git import Repo
from os.path import exists

"""
RepoClonerHandler class
"""
class RepoClonerHandler:
  def __init__(self, repository, target_folder) -> None:
    self.__repository = repository
    self.__target_folder = target_folder

  def clone(self, progress) -> None:
    Repo.clone_from(self.__repository, self.__target_folder, progress)
    
  def pull(self) -> None:
    repo = Repo(self.__target_folder)
    origin = repo.remotes.origin
    origin.pull()

  def clone_or_pull(self, progress) -> None:
    if not exists(self.__target_folder):
      self.clone(progress)
    else:
      self.pull()

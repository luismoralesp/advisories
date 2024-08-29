from os import listdir
from os.path import isfile, join

"""
DeepCollecterHandler class
"""
class DeepCollecterHandler:
  def __init__(self, folder) -> None:
    self.__folder = folder
  
  def __collect(self, folder, func) -> None:
    files = listdir(folder)
    
    for file_name in files:
      file_path = join(folder, file_name)
      if isfile(file_path):
        func(file_name, file_path)
      else:
        self.__collect(file_path, func)

  def collect(self, func) -> None:
    self.__collect(self.__folder, func)
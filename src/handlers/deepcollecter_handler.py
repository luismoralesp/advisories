import os

"""
DeepCollecterHandler class
"""
class DeepCollecterHandler:
  def __init__(self, folder) -> None:
    self.__folder = folder
  
  def __collect(self, folder, func) -> None:
    files = os.listdir(folder)
    
    for file_name in files:
      file_path = os.path.join(folder, file_name)
      if os.path.isfile(file_path):
        func(file_name, file_path)
      else:
        self.__collect(file_path, func)

  def collect(self, func) -> None:
    self.__collect(self.__folder, func)
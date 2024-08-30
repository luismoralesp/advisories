import zipfile

"""
ZipFileHandler class
"""
class ZipFileHandler:
  def __init__(self, file) -> None:
    self.__zipfile = zipfile.ZipFile(file, 'w')

  def append(self, file_name, file_path) -> None:
    self.__zipfile.write(file_path, arcname=file_name)

  def close(self):
    self.__zipfile.close()    
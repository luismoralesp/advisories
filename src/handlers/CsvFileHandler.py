from csv import writer

"""
CsvFileHandler class
"""
class CsvFileHandler:
  def __init__(self, file) -> None:
    self.__file = open(file, 'w', newline='')
    self.__writer = writer(self.__file)

  def add_row(self, row) -> None:
    self.__writer.writerow(row)

  def close(self) -> None:
    self.__file.close()
  
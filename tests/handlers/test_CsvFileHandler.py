from unittest import TestCase
from unittest.mock import patch

class TestCsvFileHandler(TestCase):

  @patch('csv.writer')
  @patch('builtins.open')
  def test_add_row(self, open, writer):
    
    from src.handlers.CsvFileHandler import CsvFileHandler

    csv_file = CsvFileHandler('/my/asome/csv/file')
    csv_file.add_row(['col1', 'col2', 'col3'])
    csv_file.close()

    open.assert_called_with('/my/asome/csv/file', 'w', newline='')
    writer.assert_called_with(open.return_value)
    writer.return_value.writerow.assert_called_with(['col1', 'col2', 'col3'])

    
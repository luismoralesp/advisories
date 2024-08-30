from unittest import TestCase
from unittest.mock import patch, Mock, call

from src.controllers.main_controller import MainController

class MockedZipFile:
  instances = {}
  
  def __init__(self, file) -> None:
    self.append = Mock()
    self.close = Mock()
    self.__class__.instances[file] = self

class TestMainController(TestCase):

  def setUp(self) -> None:
    self.RepoClonerHandler = patch('os.path.join').start()
    self.RepoClonerHandler = patch('src.handlers.repocloner_handler.RepoClonerHandler').start()
    self.DeepCollecterHandler = patch('src.handlers.deepcollecter_handler.DeepCollecterHandler').start()
    self.CsvFileHandler = patch('src.handlers.csvfile_handler.CsvFileHandler').start()
    self.ZipFileHandler = patch('src.handlers.zipfile_handler.ZipFileHandler', new=MockedZipFile).start()
    self.KevListHandler = patch('src.handlers.kevlist_handler.KevListHandler').start()
    
  def tearDown(self):
    patch.stopall()

  @patch('json.loads')
  @patch('builtins.open')
  def test_on_file(self, open, loads):
    main = MainController(Mock())

    loads.return_value = { 
      'id': 'id',
      'modified': 'modified',
      'published': 'published',
      'aliases': [ 'my_asome_alias1', 'my_asome_alias2' ],
      'database_specific': { 'severity': 'severity' },
      'summary': 'summary',
      'details': 'details',
    }
    exists = self.KevListHandler.return_value.exists
    exists.return_value = False

    main.on_file('my_asome_file.json', '/my/asome/path')

    open.assert_called_with('/my/asome/path', 'r')
    read = open.return_value.__enter__().read
    
    read.assert_called_with()
    loads.assert_called_with(read.return_value)

    exists.assert_has_calls([
      call('my_asome_alias1'),
      call('my_asome_alias2')
    ])

    add_row = self.CsvFileHandler.return_value.add_row
    add_row.assert_called_with([
      'id', 'modified', 'published', 'my_asome_alias1|my_asome_alias2',
      'severity', 'summary', 'details', ''
    ])

  @patch('json.loads')
  @patch('builtins.open')
  def test_on_file_LOW(self, open, loads):
    config = Mock()
    config.TARGET_ZIP_FILE_LOW = 'LOW'
    main = MainController(config)

    loads.return_value = {
      'database_specific': { 'severity': 'LOW' },
    }

    main.on_file('my_asome_file.json', '/my/asome/path')
    append = self.ZipFileHandler.instances['LOW'].append
    append.assert_called_with('my_asome_file.json', '/my/asome/path')

  @patch('json.loads')
  @patch('builtins.open')
  def test_on_file_MODERATE(self, open, loads):
    config = Mock()
    config.TARGET_ZIP_FILE_MODERATE = 'MODERATE'
    main = MainController(config)

    loads.return_value = {
      'database_specific': { 'severity': 'MODERATE' },
    }

    main.on_file('my_asome_file.json', '/my/asome/path')
    append = self.ZipFileHandler.instances['MODERATE'].append
    append.assert_called_with('my_asome_file.json', '/my/asome/path')

  @patch('json.loads')
  @patch('builtins.open')
  def test_on_file_HIGH(self, open, loads):
    config = Mock()
    config.TARGET_ZIP_FILE_HIGH = 'HIGH'
    main = MainController(config)

    loads.return_value = {
      'database_specific': { 'severity': 'HIGH' },
    }

    main.on_file('my_asome_file.json', '/my/asome/path')
    append = self.ZipFileHandler.instances['HIGH'].append
    append.assert_called_with('my_asome_file.json', '/my/asome/path')

  @patch('json.loads')
  @patch('builtins.open')
  def test_on_file_CRITICAL(self, open, loads):
    config = Mock()
    config.TARGET_ZIP_FILE_CRITICAL = 'CRITICAL'
    main = MainController(config)

    loads.return_value = {
      'database_specific': { 'severity': 'CRITICAL' },
    }

    main.on_file('my_asome_file.json', '/my/asome/path')
    append = self.ZipFileHandler.instances['CRITICAL'].append
    append.assert_called_with('my_asome_file.json', '/my/asome/path')

  def test_download(self):
    main = MainController(Mock())
    main.CloneProgress = Mock()

    main.download()

    clone_or_pull = self.RepoClonerHandler.return_value.clone_or_pull
    load_json = self.KevListHandler.return_value.load_json
    
    main.CloneProgress.assert_called_with()
    clone_or_pull.assert_called_with(main.CloneProgress.return_value)
    load_json.assert_called_with()

  def test_collect(self):
    config = Mock()

    config.TARGET_ZIP_FILE_LOW = 'LOW'
    config.TARGET_ZIP_FILE_MODERATE = 'MODERATE'
    config.TARGET_ZIP_FILE_HIGH = 'HIGH'
    config.TARGET_ZIP_FILE_CRITICAL = 'CRITICAL'
    
    main = MainController(config)

    main.collect()

    add_row = self.CsvFileHandler.return_value.add_row
    collect = self.DeepCollecterHandler.return_value.collect

    close_LOW = self.ZipFileHandler.instances['LOW'].close
    close_MODERATE = self.ZipFileHandler.instances['MODERATE'].close
    close_HIGH = self.ZipFileHandler.instances['HIGH'].close
    close_CRITICAL = self.ZipFileHandler.instances['CRITICAL'].close

    add_row.assert_called_with(['Id', 'Modified', 'Published', 'Aliases', 'Severity', 'Summary', 'Details', 'KEV'])
    collect.assert_called_with(main.on_file)

    close_LOW.assert_called_with()
    close_MODERATE.assert_called_with()
    close_HIGH.assert_called_with()
    close_CRITICAL.assert_called_with()

  def test_start(self):
    main = MainController(Mock())

    main.download = Mock()
    main.collect = Mock()

    main.start()

    main.download.assert_called_with()
    main.collect.assert_called_with()


     
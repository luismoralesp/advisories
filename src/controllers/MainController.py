from os.path import join
from git.remote import RemoteProgress
import json

from src.handlers.RepoClonerHandler import RepoClonerHandler
from src.handlers.DeepCollecterHandler import DeepCollecterHandler
from src.handlers.CsvFileHandler import CsvFileHandler
from src.handlers.ZipFileHandler import ZipFileHandler
from src.handlers.KevListHandler import KevListHandler

"""
MainController class
"""
class MainController:
  def __init__(self, config) -> None:
    self.__config = config

  def start(self):
    repo_cloner = RepoClonerHandler(
      repository=self.__config.REPOSITORY,
      target_folder=self.__config.TARGET_FOLDER
    )

    kev_list = KevListHandler(self.__config.KEV_URL)

    print("Downloading from git...")
    repo_cloner.clone_or_pull(self.CloneProgress())
    print("Doenloading from Kev...")
    kev_list.load_json()

    deep_collenter = DeepCollecterHandler(join(
      self.__config.TARGET_FOLDER,
      self.__config.ADVISORES_FOLDER
    ))

    zip_file_low = ZipFileHandler(self.__config.TARGET_ZIP_FILE_LOW)
    zip_file_moderate = ZipFileHandler(self.__config.TARGET_ZIP_FILE_MODERATE)
    zip_file_high = ZipFileHandler(self.__config.TARGET_ZIP_FILE_HIGH)
    zip_file_critical = ZipFileHandler(self.__config.TARGET_ZIP_FILE_CRITICAL)

    csv_file = CsvFileHandler(self.__config.CSV_FILE)  
    csv_file.add_row(['Id', 'Modified', 'Published', 'Aliases', 'Severity', 'Summary', 'Details', 'KEV'])

    def on_file(file_name, file_path):
      with open(file_path, 'r') as json_file:
        content = json_file.read()
        json_data = json.loads(content)

        severity = json_data['database_specific']['severity']
        aliases = ','.join(json_data.get('aliases', []))

        kev = ''
        for alias in json_data.get('aliases', []):
          if alias.startswith('CVE-'):
            if kev_list.exists(alias):
              kev = '1'

        csv_file.add_row([
          json_data.get('id', ''),
          json_data.get('modified', ''),
          json_data.get('published', ''),
          aliases,
          severity,
          json_data.get('summary', ''),
          json_data.get('details', ''),
          kev
        ])

        if severity  == 'LOW':
          zip_file_low.append(file_name, file_path)
        elif severity == 'MODERATE':
          zip_file_moderate.append(file_name, file_path)
        elif severity == 'HIGH':
          zip_file_high.append(file_name, file_path)
        elif severity == 'CRITICAL':
          zip_file_critical.append(file_name, file_path)

    print("Colecting files...")
    deep_collenter.collect(on_file)

    zip_file_low.close()
    zip_file_moderate.close()
    zip_file_high.close()
    zip_file_critical.close()

  class CloneProgress(RemoteProgress):
    def update(self, *args):
        print(self._cur_line, end='\r')
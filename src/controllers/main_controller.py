import json
import os
import git

from src.handlers import repocloner_handler
from src.handlers import deepcollecter_handler
from src.handlers import csvfile_handler
from src.handlers import zipfile_handler
from src.handlers import kevlist_handler

"""
MainController class
"""
class MainController:
  def __init__(self, config) -> None:
    self.repo_cloner = repocloner_handler.RepoClonerHandler(
      repository=config.REPOSITORY,
      target_folder=config.TARGET_FOLDER
    )
    self.kev_list = kevlist_handler.KevListHandler(config.KEV_URL)
    self.deep_collenter = deepcollecter_handler.DeepCollecterHandler(os.path.join(
      config.TARGET_FOLDER,
      config.ADVISORES_FOLDER
    ))
    self.zip_file_low = zipfile_handler.ZipFileHandler(config.TARGET_ZIP_FILE_LOW)
    self.zip_file_moderate = zipfile_handler.ZipFileHandler(config.TARGET_ZIP_FILE_MODERATE)
    self.zip_file_high = zipfile_handler.ZipFileHandler(config.TARGET_ZIP_FILE_HIGH)
    self.zip_file_critical = zipfile_handler.ZipFileHandler(config.TARGET_ZIP_FILE_CRITICAL)
    self.csv_file = csvfile_handler.CsvFileHandler(config.CSV_FILE)

  def on_file(self, file_name, file_path):
    with open(file_path, 'r') as json_file:
      content = json_file.read()
      json_data = json.loads(content)

      id = json_data.get('id', '')
      modified = json_data.get('modified', '')
      published = json_data.get('published', '')
      aliases = json_data.get('aliases', [])
      severity = json_data.get('database_specific', { 'severity': '' }).get('severity', '')
      summary = json_data.get('summary', '')
      details = json_data.get('details', '')

      kev = ''
      for alias in aliases:
        if self.kev_list.exists(alias):
          kev = '1'
          break

      self.csv_file.add_row([
        id, modified, published, '|'.join(aliases),
        severity, summary, details, kev
      ])

      if severity  == 'LOW':
        self.zip_file_low.append(file_name, file_path)
      elif severity == 'MODERATE':
        self.zip_file_moderate.append(file_name, file_path)
      elif severity == 'HIGH':
        self.zip_file_high.append(file_name, file_path)
      elif severity == 'CRITICAL':
        self.zip_file_critical.append(file_name, file_path)

  def download(self):
    print("Downloading from git...")
    self.repo_cloner.clone_or_pull(self.CloneProgress())

    print("Doenloading from Kev...")
    self.kev_list.load_json()

  def collect(self):
    print("Colecting files...")
    self.csv_file.add_row(['Id', 'Modified', 'Published', 'Aliases', 'Severity', 'Summary', 'Details', 'KEV'])

    self.deep_collenter.collect(self.on_file)

    print("Closing files...")
    self.zip_file_low.close()
    self.zip_file_moderate.close()
    self.zip_file_high.close()
    self.zip_file_critical.close()

  def start(self):
    self.download()
    self.collect()
    
  class CloneProgress(git.remote.RemoteProgress):
    def update(self, *args):
        print(self._cur_line, end='\r')
from urllib import request 
import json

"""
KevListHandler class
"""
class KevListHandler:
  def __init__(self, url):
    self.__url = url

  def load_json(self) -> None:
    response = request.urlopen(self.__url)
    self.__data = json.loads(response.read())

  def exists(self, cve_id) -> bool:
    for vulnerability in self.__data['vulnerabilities']:
      if vulnerability['cveID'] == cve_id:
        return True
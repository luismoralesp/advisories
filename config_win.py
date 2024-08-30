from os import path

dir_path = path.dirname(path.realpath(__file__))

OS = 'WINDOWS'

# Repo Clonner Config
REPOSITORY = 'https://github.com/github/advisory-database'
TARGET_FOLDER = path.join(dir_path, 'repo_target')

# Kev
KEV_URL = 'https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json'

# Deep Collecter
ADVISORES_FOLDER = 'advisories\\github-reviewed'

# Csv File
CSV_FILE = path.join(dir_path, 'result\\advisories.csv')

# Zip File
TARGET_ZIP_FILE_LOW = path.join(dir_path, 'result\\low.zip')
TARGET_ZIP_FILE_MODERATE = path.join(dir_path, 'result\\moderate.zip')
TARGET_ZIP_FILE_HIGH = path.join(dir_path, 'result\\high.zip')
TARGET_ZIP_FILE_CRITICAL = path.join(dir_path, 'result\\critical.zip')
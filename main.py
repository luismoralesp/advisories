from src.controllers.main_controller import MainController
import os
import config
import config_win


if __name__ == '__main__':
  MainController(config_win if os.name == 'nt' else config).start()
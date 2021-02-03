import os
from pathlib import Path

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))



DRIVER_PATH = os.environ.get('CHROMEDRIVER_PATH') or os.path.join(Path.home(), 'driver/chromedriver')

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"

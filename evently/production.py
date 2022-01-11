import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = False
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
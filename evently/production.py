import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = False
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

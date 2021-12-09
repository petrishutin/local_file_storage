"""This module provides auth storage. Storage lives in memory during runtime, so it makes this app stateful  """

from app.settings import config
from app.utils.hash_pass import hash_password

auth_storage = {config.ADMIN_NAME: hash_password(config.ADMIN_PASSWORD)}

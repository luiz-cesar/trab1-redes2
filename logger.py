# Autores:
# JEAN GUILHERME CARRARO DA SILVA
# LUIZ CESAR CLABOND ALMEIDA

from datetime import datetime

def log(*args):
  print(*args, "--", datetime.today())
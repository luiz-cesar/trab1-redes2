from datetime import datetime

def log(*args):
  print(*args, "--", datetime.today())
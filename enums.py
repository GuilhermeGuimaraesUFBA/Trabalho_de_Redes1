from enum import Enum

class Command(str, Enum):
  DEPOSIT = "DEPOSIT"
  RECOVERY = "RECOVERY"

class Status(str, Enum):
  OK = "OK"
  ERROR = "ERROR"
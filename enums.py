from enum import Enum

class Command(str, Enum):
  DEPOSIT = "DEPOSIT"
  RECOVERY = "RECOVERY"
  REMOVE = "REMOVE"

class Status(str, Enum):
  OK = "OK"
  ERROR = "ERROR"
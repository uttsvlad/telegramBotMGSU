from enum import Enum

# token = "1234567:ABCxyz"
# db_file = "database.vdb"


class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0"  
    S_ENTER_NAME = "1"
    S_ENTER_GROUP = "2"
    
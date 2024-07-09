from pathlib import Path

MAIN_DOC_URL = 'https://docs.python.org/3/'

PEP_URL = 'https://peps.python.org/'

BASE_DIR = Path(__file__).parent

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}

PEP_REGUL = r'^pep-[0-9]{4}\/$'

LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'

DT_FORMAT = "%d.%m.%Y %H:%M:%S"

LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'parser.log'

PRETTY_OUTPRINT = 'pretty'
CSV_OUTPRINT = 'file'

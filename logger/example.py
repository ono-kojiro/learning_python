from logging import basicConfig, getLogger, DEBUG
from systemd.journal import JournalHandler

basicConfig(level=DEBUG)

logger = getLogger(__name__)
logger.addHandler(JournalHandler())
logger.propagate = False

logger.debug('This is debug log')


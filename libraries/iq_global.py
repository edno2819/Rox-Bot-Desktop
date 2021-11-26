from libraries.iq_api import IqOption
from libraries.iq_run import MainOperation
import logging


MAIN = IqOption()
MAIN_RUN = MainOperation(MAIN)
LOG = logging.getLogger(__name__)



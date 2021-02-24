import os
os.chdir('src')

from pathlib import Path
import logging

logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s][%(name)s] - %(message)s'
)

SRC_PATH = Path(__file__).parent.absolute()

__all__ = ['SRC_PATH']

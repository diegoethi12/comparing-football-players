from pathlib import Path
import logging

logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s][%(name)s] - %(message)s'
)

SRC_PATH = Path(__file__).parent.absolute()
DATA_PATH = SRC_PATH / 'data'
MODEL_PATH = SRC_PATH / 'models'

__all__ = ['SRC_PATH', 'DATA_PATH']

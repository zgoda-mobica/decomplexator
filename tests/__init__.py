import os
from datetime import datetime

from decomplexator.utils import NodeComplexity


def _path(*elem):
    here = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(here, *elem))


class BaseTests:

    DUMMY_DATA_HOME = '/dummy'
    STORAGE_FILENAME = 'test.dat'

    FILE_NAME = 'test1.py'
    DUMMY_PATH = os.path.join(DUMMY_DATA_HOME, FILE_NAME)
    FILE_CONTENT = open(_path('data', FILE_NAME)).read()
    DT = datetime(2018, 8, 2, 12, 22, 0)
    DT_FMT = DT.isoformat(timespec='seconds')
    COMPLEXITY = {
        DUMMY_PATH: {
            DT_FMT: {
                'fun1': NodeComplexity(0, 1, 'fun1'),
                'fun2': NodeComplexity(1, 2, 'fun2'),
            },
        },
    }

    @classmethod
    def _environ(cls):
        return {
            'XDG_DATA_HOME': cls.DUMMY_DATA_HOME,
        }

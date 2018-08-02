class BaseTests:

    DUMMY_DATA_HOME = '/dummy'
    STORAGE_FILENAME = 'test.dat'

    @classmethod
    def _environ(cls):
        return {
            'XDG_DATA_HOME': cls.DUMMY_DATA_HOME,
        }

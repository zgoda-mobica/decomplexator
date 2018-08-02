import os
import pickle


class StorageTests:

    DUMMY_DATA_HOME = '/dummy'
    STORAGE_FILENAME = 'test.dat'

    @classmethod
    def _environ(cls):
        return {
            'XDG_DATA_HOME': cls.DUMMY_DATA_HOME,
        }


class TestStoragePath(StorageTests):

    def test_with_filename(self, mocker):
        mocker.patch.dict('os.environ', self._environ())
        from dcx.utils import get_storage_path
        generated = get_storage_path(self.STORAGE_FILENAME)
        head, tail = os.path.split(generated)
        assert head == self.DUMMY_DATA_HOME
        assert tail == self.STORAGE_FILENAME

    def test_without_filename(self, mocker):
        mocker.patch.dict('os.environ', self._environ())
        from dcx.utils import get_storage_path, STORAGE_FNAME
        generated = get_storage_path()
        head, tail = os.path.split(generated)
        assert head == self.DUMMY_DATA_HOME
        assert tail == STORAGE_FNAME


class TestLoadPreviousScores(StorageTests):

    def test_no_file(self, mocker):
        mocker.patch.dict('os.environ', self._environ())
        from dcx.utils import load_previous_scores
        data = load_previous_scores()
        assert data == {}

    def test_file_corrupted(self, mocker):
        fake = mocker.mock_open(read_data=b'rubbish')
        mocker.patch('builtins.open', fake)
        mocker.patch.dict('os.environ', self._environ())
        from dcx.utils import load_previous_scores
        data = load_previous_scores()
        assert data == {}
        fake.assert_called_once()

    def test_wrong_data(self, mocker):
        fake = mocker.mock_open(read_data=pickle.dumps('a string'))
        mocker.patch('builtins.open', fake)
        mocker.patch.dict('os.environ', self._environ())
        from dcx.utils import load_previous_scores
        data = load_previous_scores()
        assert data == {}
        fake.assert_called_once()

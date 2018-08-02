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
        from decomplexator.utils import get_storage_path
        generated = get_storage_path(self.STORAGE_FILENAME)
        head, tail = os.path.split(generated)
        assert head == self.DUMMY_DATA_HOME
        assert tail == self.STORAGE_FILENAME

    def test_without_filename(self, mocker):
        mocker.patch.dict('os.environ', self._environ())
        from decomplexator.utils import get_storage_path, STORAGE_FNAME
        generated = get_storage_path()
        head, tail = os.path.split(generated)
        assert head == self.DUMMY_DATA_HOME
        assert tail == STORAGE_FNAME


class TestLoadPreviousScores(StorageTests):

    def test_no_file(self, mocker):
        mocker.patch.dict('os.environ', self._environ())
        from decomplexator.utils import load_previous_scores
        data = load_previous_scores()
        assert data == {}

    def test_file_corrupted(self, mocker):
        fake = mocker.mock_open(read_data=b'rubbish')
        mocker.patch('builtins.open', fake)
        mocker.patch.dict('os.environ', self._environ())
        from decomplexator.utils import load_previous_scores
        data = load_previous_scores()
        assert data == {}
        fake.assert_called_once()

    def test_wrong_data(self, mocker):
        fake = mocker.mock_open(read_data=pickle.dumps('a string'))
        mocker.patch('builtins.open', fake)
        mocker.patch.dict('os.environ', self._environ())
        from decomplexator.utils import load_previous_scores
        data = load_previous_scores()
        assert data == {}
        fake.assert_called_once()


class TestClearStorage(StorageTests):

    def test_remove_storage(self, mocker):
        fake_remove = mocker.MagicMock()
        mocker.patch('decomplexator.utils.os.remove', fake_remove)
        mocker.patch.dict('os.environ', self._environ())
        from decomplexator.utils import get_storage_path, clear_storage
        generated = get_storage_path(self.STORAGE_FILENAME)
        clear_storage(self.STORAGE_FILENAME)
        fake_remove.assert_called_once_with(generated)


class TestSaveScores(StorageTests):

    SCORES_1 = {
        'module.py': {
            '2018-08-02T12:24': {
                'fun': (3, 2, 'fun'),
            }
        }
    }

    def test_no_file(self, mocker):
        fake = mocker.mock_open()
        mocker.patch('builtins.open', fake)
        fake_os = mocker.MagicMock()
        mocker.patch('decomplexator.utils.os', fake_os)
        fake_os.makedirs = mocker.MagicMock()
        mocker.patch.dict('os.environ', self._environ())
        from decomplexator.utils import save_scores
        save_scores(self.SCORES_1)
        fake_os.makedirs.assert_called_once_with(self.DUMMY_DATA_HOME, exist_ok=True)
        handle = fake()
        handle.write.assert_called_once_with(pickle.dumps(self.SCORES_1))

    def test_file_corrupted(self, mocker):
        fake = mocker.mock_open(read_data=b'rubbish')
        mocker.patch('builtins.open', fake)
        fake_os = mocker.MagicMock()
        mocker.patch('decomplexator.utils.os', fake_os)
        fake_os.makedirs = mocker.MagicMock()
        mocker.patch.dict('os.environ', self._environ())
        from decomplexator.utils import save_scores
        save_scores(self.SCORES_1)
        handle = fake()
        handle.write.assert_called_once_with(pickle.dumps(self.SCORES_1))

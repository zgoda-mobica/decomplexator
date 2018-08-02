import os
import pickle

import pytest

from decomplexator.utils import get_storage_path, clear_storage, STORAGE_FNAME, load_previous_scores, save_scores

from tests import BaseTests


class StorageTests(BaseTests):
    pass


class TestStoragePath(StorageTests):

    def test_with_filename(self, mocker):
        mocker.patch.dict('os.environ', self._environ())
        generated = get_storage_path(self.STORAGE_FILENAME)
        head, tail = os.path.split(generated)
        assert head == self.DUMMY_DATA_HOME
        assert tail == self.STORAGE_FILENAME

    def test_without_filename(self, mocker):
        mocker.patch.dict('os.environ', self._environ())
        generated = get_storage_path()
        head, tail = os.path.split(generated)
        assert head == self.DUMMY_DATA_HOME
        assert tail == STORAGE_FNAME


class TestLoadPreviousScores(StorageTests):

    def test_no_file(self, mocker):
        mocker.patch.dict('os.environ', self._environ())
        data = load_previous_scores()
        assert data == {}

    def test_file_corrupted(self, mocker):
        fake = mocker.mock_open(read_data=b'rubbish')
        mocker.patch('builtins.open', fake)
        mocker.patch.dict('os.environ', self._environ())
        data = load_previous_scores()
        assert data == {}
        fake.assert_called_once()

    def test_wrong_data(self, mocker):
        fake = mocker.mock_open(read_data=pickle.dumps('a string'))
        mocker.patch('builtins.open', fake)
        mocker.patch.dict('os.environ', self._environ())
        data = load_previous_scores()
        assert data == {}
        fake.assert_called_once()


class TestClearStorage(StorageTests):

    def test_remove_storage(self, mocker):
        fake_remove = mocker.MagicMock()
        mocker.patch('decomplexator.utils.os.remove', fake_remove)
        mocker.patch.dict('os.environ', self._environ())
        generated = get_storage_path(self.STORAGE_FILENAME)
        clear_storage(self.STORAGE_FILENAME)
        fake_remove.assert_called_once_with(generated)

    def test_remove_storage_no_file(self, mocker):
        fake_remove = mocker.MagicMock(side_effect=FileNotFoundError)
        mocker.patch('decomplexator.utils.os.remove', fake_remove)
        mocker.patch.dict('os.environ', self._environ())
        generated = get_storage_path(self.STORAGE_FILENAME)
        with pytest.raises(FileNotFoundError):
            clear_storage(self.STORAGE_FILENAME)
        fake_remove.assert_called_once_with(generated)


class TestSaveScores(StorageTests):

    SCORES_1 = {
        'module.py': {
            'date2': {
                'fun1': (3, 2, 'fun1'),
            }
        }
    }

    SCORES_2 = {
        'anothermodule.py': {
            'date1': {
                'fun2': (1, 0, 'fun2'),
            }
        }
    }

    SCORES_3 = {
        'module.py': {
            'date1': {
                'fun1': (2, 1, 'fun1'),
            }
        }
    }

    def _combine_scores(self, *scores):
        ret = {}
        for score_dict in scores:
            key, run_data = list(score_dict.items())[0]
            score_data = ret.setdefault(key, run_data)
            score_data.update(run_data)
        return ret

    def test_no_file(self, mocker):
        fake = mocker.mock_open()
        mocker.patch('builtins.open', fake)
        fake_os = mocker.MagicMock()
        fake_os.environ.get.return_value = self.DUMMY_DATA_HOME
        mocker.patch('decomplexator.utils.os', fake_os)
        fake_os.makedirs = mocker.MagicMock()
        save_scores(self.SCORES_1)
        fake_os.makedirs.assert_called_once_with(self.DUMMY_DATA_HOME, exist_ok=True)
        handle = fake()
        handle.write.assert_called_once_with(pickle.dumps(self.SCORES_1))

    def test_file_corrupted(self, mocker):
        fake = mocker.mock_open(read_data=b'rubbish')
        mocker.patch('builtins.open', fake)
        fake_os = mocker.MagicMock()
        fake_os.environ.get.return_value = self.DUMMY_DATA_HOME
        mocker.patch('decomplexator.utils.os', fake_os)
        fake_os.makedirs = mocker.MagicMock()
        save_scores(self.SCORES_1)
        handle = fake()
        handle.write.assert_called_once_with(pickle.dumps(self.SCORES_1))

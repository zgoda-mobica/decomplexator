import os

import pytest

from decomplexator import run

from tests import BaseTests


class RunTests(BaseTests):

    DN = 'test'
    FNAMES = ('test1.py', 'test2.py', 'test3.py')


class TestCmdlineArgs(RunTests):

    def test_args_parser(self):
        parser = run.make_parser()
        assert len(parser._actions) == 5

    def test_args_clear(self):
        parser = run.make_parser()
        args = parser.parse_args(['--clear'])
        assert args.clear is True

    def test_args_continuous(self):
        parser = run.make_parser()
        args = parser.parse_args(['-c'])
        assert args.continuous is True

    def test_args_input(self):
        test_fn = 'test.py'
        parser = run.make_parser()
        args = parser.parse_args(['-i', test_fn])
        assert args.filename == test_fn

    def test_args_directory(self):
        test_dn = 'test'
        parser = run.make_parser()
        args = parser.parse_args(['-d', test_dn])
        assert args.project_dir == test_dn


class TestRunInterface(RunTests):

    @pytest.mark.parametrize('continuous', (False, True))
    def test_analyze_file(self, mocker, continuous):
        test_fn = 'test.py'
        fake = mocker.MagicMock()
        mocker.patch('decomplexator.run.analyze_files', fake)
        run.analyze_file(test_fn, continuous)
        fake.assert_called_once_with([test_fn], continuous)

    @pytest.mark.parametrize('continuous', (False, True))
    def test_analyze_directory(self, mocker, continuous):
        fpaths = [os.path.join(self.DN, x) for x in self.FNAMES]
        fake = mocker.MagicMock()
        mocker.patch('decomplexator.run.analyze_files', fake)
        mocker.patch('decomplexator.run.glob.iglob', mocker.MagicMock(return_value=self.FNAMES))
        run.analyze_directory(self.DN, continuous)
        fake.assert_called_once_with(fpaths, continuous)

    @pytest.mark.parametrize('continuous', (False, True))
    def test_analyze_files(self, mocker, continuous):
        fpaths = [os.path.join(self.DN, x) for x in self.FNAMES]
        fake = mocker.MagicMock(autospec='decomplexator.analyzer.AnalyzerGroup')
        fake.analyze = mocker.Mock()
        fake.summary = mocker.Mock()
        fake.persist = mocker.Mock()
        mocker.patch('decomplexator.run.AnalyzerGroup', fake)
        run.analyze_files(fpaths, continuous)
        fake().analyze.assert_called_once()
        fake().summary.assert_called_once()
        assert fake().persist.called == continuous

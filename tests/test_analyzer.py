import random

from decomplexator.analyzer import ComplexityAnalyzer, AnalyzerGroup

from tests import BaseTests


class AnalyzerBaseTests(BaseTests):

    MAX_COMPLEXITY = 10

    def _gen_complexity(cls, date, num_records=2, max_entries_per_record=2):
        ret = {}
        for i in range(num_records):
            filename = 'test%d.py' % i
            run_data = ret.setdefault(filename, {date: {}})
            num_entries = random.randint(0, max_entries_per_record)
            for n in range(num_entries):
                entry_name = 'fun%d' % n
                data = (random.randint(0, cls.MAX_COMPLEXITY), random.randint(0, cls.MAX_COMPLEXITY), entry_name)
                run_data[date][entry_name] = data
        return ret


class TestAnalyzer(AnalyzerBaseTests):

    def test_analyze(self, mocker):
        fake_dt = mocker.MagicMock()
        mocker.patch('decomplexator.analyzer.datetime', fake_dt)
        fake_dt.utcnow = mocker.MagicMock(return_value=self.DT)
        fake = mocker.mock_open(read_data=self.FILE_CONTENT)
        mocker.patch('builtins.open', fake)
        mocker.patch.dict('os.environ', self._environ())
        ca = ComplexityAnalyzer(self.DUMMY_PATH)
        ca.analyze()
        summary = ca.summary()
        run_data = summary[self.DUMMY_PATH][self.DT_FMT]
        for name in ['fun1', 'fun2']:
            assert run_data[name] == self.COMPLEXITY[self.DUMMY_PATH][self.DT_FMT][name]

    def test_analyze_with_fname(self, mocker):
        fake_dt = mocker.MagicMock()
        mocker.patch('decomplexator.analyzer.datetime', fake_dt)
        fake_dt.utcnow = mocker.MagicMock(return_value=self.DT)
        fake = mocker.mock_open(read_data=self.FILE_CONTENT)
        mocker.patch('builtins.open', fake)
        mocker.patch.dict('os.environ', self._environ())
        ca = ComplexityAnalyzer()
        ca.analyze(self.DUMMY_PATH)
        summary = ca.summary()
        run_data = summary[self.DUMMY_PATH][self.DT_FMT]
        for name in ['fun1', 'fun2']:
            assert run_data[name] == self.COMPLEXITY[self.DUMMY_PATH][self.DT_FMT][name]

    def test_has_data(self, mocker):
        fake_dt = mocker.MagicMock()
        mocker.patch('decomplexator.analyzer.datetime', fake_dt)
        fake_dt.utcnow = mocker.MagicMock(return_value=self.DT)
        fake = mocker.mock_open(read_data=self.FILE_CONTENT)
        mocker.patch('builtins.open', fake)
        mocker.patch.dict('os.environ', self._environ())
        ca = ComplexityAnalyzer()
        assert ca.has_data() is False
        ca.analyze(self.DUMMY_PATH)
        assert ca.has_data() is True

    def test_get_summary_data_generated(self, mocker):
        fake_dt = mocker.MagicMock()
        mocker.patch('decomplexator.analyzer.datetime', fake_dt)
        fake_dt.utcnow = mocker.MagicMock(return_value=self.DT)
        fake = mocker.mock_open(read_data=self.FILE_CONTENT)
        mocker.patch('builtins.open', fake)
        mocker.patch.dict('os.environ', self._environ())
        ca = ComplexityAnalyzer()
        ca.analyze(self.DUMMY_PATH)
        ca.summary()
        ca.summary()
        fake_dt.utcnow.assert_called_once()

    def test_persist(self, mocker):
        mock_save = mocker.MagicMock()
        mocker.patch('decomplexator.analyzer.save_scores', mock_save)
        mock_load = mocker.MagicMock(return_value={})
        mocker.patch('decomplexator.analyzer.load_previous_scores', mock_load)
        mock_open = mocker.mock_open(read_data=self.FILE_CONTENT)
        mocker.patch('builtins.open', mock_open)
        mocker.patch.dict('os.environ', self._environ())
        ca = ComplexityAnalyzer()
        ca.analyze(self.DUMMY_PATH)
        ca.persist()
        mock_save.assert_called_once()

    def test_persist_no_data(self, mocker):
        mock_save = mocker.MagicMock()
        mocker.patch('decomplexator.analyzer.save_scores', mock_save)
        mocker.patch.dict('os.environ', self._environ())
        ca = ComplexityAnalyzer()
        ca.persist()
        assert mock_save.call_count == 0


class TestAnalyzerGroup(AnalyzerBaseTests):

    FILE_NAMES = [
        'test1.py',
        'test2.py',
        'test3.py',
    ]

    def test_add_files(self, mocker):
        mocker.patch.dict('os.environ', self._environ())
        grp = AnalyzerGroup()
        grp.add_files(self.FILE_NAMES)
        assert len(grp.files) == len(self.FILE_NAMES)

    def test_analyze(self, mocker):
        fake_analyzer = mocker.MagicMock()
        fake_analyzer.analyze = mocker.MagicMock()
        mocker.patch('decomplexator.analyzer.ComplexityAnalyzer', fake_analyzer)
        grp = AnalyzerGroup(self.FILE_NAMES)
        grp.analyze()
        assert len(grp.analyzers) == len(self.FILE_NAMES)
        fake_analyzer.analyze.call_count == len(self.FILE_NAMES)

    def test_summary(self, mocker):
        complexity = self._gen_complexity(self.DT_FMT)
        file_names = list(complexity.keys())
        fake_analyzer = mocker.MagicMock()
        fake_analyzer.summary = mocker.MagicMock(return_value=complexity)
        mocker.patch('decomplexator.analyzer.ComplexityAnalyzer', fake_analyzer)
        grp = AnalyzerGroup(file_names)
        grp.summary()
        fake_analyzer.summary.call_count == len(file_names)

    def test_summary_live_data(self, mocker):
        mock_open = mocker.mock_open(read_data=self.FILE_CONTENT)
        mocker.patch('builtins.open', mock_open)
        mocker.patch.dict('os.environ', self._environ())
        ca = ComplexityAnalyzer()
        ca.analyze(self.DUMMY_PATH)
        summary_single = ca.summary()
        grp = AnalyzerGroup([self.DUMMY_PATH])
        grp.analyze()
        summary_group = grp.summary()
        assert len(summary_single) == len(summary_group)
        assert sorted(summary_single.keys()) == sorted(summary_group.keys())

    def test_summary_no_files(self, mocker):
        fake_analyzer = mocker.MagicMock()
        fake_analyzer.summary = mocker.MagicMock()
        mocker.patch('decomplexator.analyzer.ComplexityAnalyzer', fake_analyzer)
        grp = AnalyzerGroup(self.FILE_NAMES)
        data = grp.summary()
        assert len(data) == 0

    def test_persist_no_previous_data(self, mocker):
        fake_load = mocker.MagicMock(return_value={})
        mocker.patch('decomplexator.analyzer.load_previous_scores', fake_load)
        fake_save = mocker.MagicMock()
        mocker.patch('decomplexator.analyzer.save_scores', fake_save)
        fake_open = mocker.mock_open(read_data=self.FILE_CONTENT)
        mocker.patch('builtins.open', fake_open)
        mocker.patch.dict('os.environ', self._environ())
        grp = AnalyzerGroup([self.FILE_NAME])
        grp.analyze()
        grp.persist()
        fake_save.assert_called_once_with(grp.summary(), mocker.ANY)

    def test_persist_check_analyzer_has_data(self, mocker):
        fake_load = mocker.MagicMock(return_value={})
        mocker.patch('decomplexator.analyzer.load_previous_scores', fake_load)
        fake_save = mocker.MagicMock()
        mocker.patch('decomplexator.analyzer.save_scores', fake_save)
        fake_analyzer = mocker.MagicMock()
        fake_analyzer.has_data = mocker.MagicMock(return_value=True)
        fake_analyzer.summary = mocker.MagicMock(return_value={self.DUMMY_PATH: {'x': 'file data'}})
        mocker.patch('decomplexator.analyzer.ComplexityAnalyzer', fake_analyzer)
        fake_open = mocker.mock_open()
        mocker.patch('builtins.open', fake_open)
        mocker.patch.dict('os.environ', self._environ())
        grp = AnalyzerGroup([self.DUMMY_PATH])
        grp.analyze()
        grp.persist()
        save_args, _ = fake_save.call_args
        assert list(save_args[0].keys())[0] == self.DUMMY_PATH

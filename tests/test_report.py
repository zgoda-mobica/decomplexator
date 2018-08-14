import copy
import io
from datetime import timedelta

from tests import BaseTests

from decomplexator.report import ComplexityReport
from decomplexator.utils import NodeComplexity


class TestReport(BaseTests):

    FILE_HEADER_LEN = 3

    def _complete_scores(self):
        new_scores = copy.deepcopy(self.COMPLEXITY)
        prev_date = self.DT - timedelta(days=1)
        new_scores[self.DUMMY_PATH][prev_date.isoformat(timespec='seconds')] = {
            'fun1': NodeComplexity(1, 3, 'fun1'),
            'fun2': NodeComplexity(4, 1, 'fun2'),
        }
        return new_scores

    def test_file_header(self):
        fh = ComplexityReport.file_header(self.DUMMY_PATH)
        assert len(fh) == self.FILE_HEADER_LEN
        assert len(fh[1]) == len(fh[2])
        assert self.DUMMY_PATH in fh[1]

    def test_report_scores(self):
        rp = ComplexityReport(self.COMPLEXITY)
        assert rp.scores == self.COMPLEXITY

    def test_simple_report(self):
        rp = ComplexityReport(self.COMPLEXITY)
        data = rp.print_report(print_it=False)
        assert len(data) == len(self.COMPLEXITY[self.DUMMY_PATH][self.DT_FMT].keys()) + self.FILE_HEADER_LEN
        assert self.DUMMY_PATH in data[1]

    def test_simple_report_print(self, mocker):
        fake_stdout = io.StringIO()
        mocker.patch('sys.stdout', fake_stdout)
        rp = ComplexityReport(self.COMPLEXITY)
        rp.print_report()
        assert self.DUMMY_PATH in fake_stdout.getvalue()

    def test_continuous_report(self):
        scores = self._complete_scores()
        rp = ComplexityReport(scores)
        data = rp.print_report(continuous=True, print_it=False)
        assert len(data) == len(self.COMPLEXITY[self.DUMMY_PATH][self.DT_FMT].keys()) + self.FILE_HEADER_LEN
        assert self.DUMMY_PATH in data[1]

    def test_continuous_report_print(self, mocker):
        fake_stdout = io.StringIO()
        mocker.patch('sys.stdout', fake_stdout)
        scores = self._complete_scores()
        rp = ComplexityReport(scores)
        rp.print_report(continuous=True)
        assert self.DUMMY_PATH in fake_stdout.getvalue()

    def test_calc_change_1st_run(self):
        node = 'fun1'
        cur = self.COMPLEXITY[self.DUMMY_PATH][self.DT_FMT]
        prev = None
        change = ComplexityReport.calc_changes(node, cur, prev)
        assert change.cognitive == 0
        assert change.cyclomatic == 0

    def test_calc_change_no_change(self):
        node = 'fun1'
        cur = self.COMPLEXITY[self.DUMMY_PATH][self.DT_FMT]
        prev = copy.deepcopy(cur)
        change = ComplexityReport.calc_changes(node, cur, prev)
        assert change.cognitive == 0
        assert change.cyclomatic == 0

    def test_calc_change(self):
        node = 'fun1'
        cur = self.COMPLEXITY[self.DUMMY_PATH][self.DT_FMT]
        prev = {node: NodeComplexity(1, 4, node)}
        change = ComplexityReport.calc_changes(node, cur, prev)
        assert change.cognitive == cur[node].cognitive - prev[node].cognitive
        assert change.cyclomatic == cur[node].cyclomatic - prev[node].cyclomatic

    def test_continuous_lines_no_data(self):
        data = copy.deepcopy(self.COMPLEXITY[self.DUMMY_PATH])
        data[self.DT_FMT] = {}
        rp = ComplexityReport(self.COMPLEXITY)
        line = rp.continuous_report_lines(self.DUMMY_PATH, data)
        assert line is None

    def test_continuous_lines_no_previous(self):
        rp = ComplexityReport(self.COMPLEXITY)
        lines = rp.continuous_report_lines(self.DUMMY_PATH, self.COMPLEXITY[self.DUMMY_PATH])
        assert len(lines) == 2 + self.FILE_HEADER_LEN
        out = ' '.join(lines)
        assert out.count('(+0)') == 4

    def test_simple_lines_no_data(self):
        data = copy.deepcopy(self.COMPLEXITY[self.DUMMY_PATH])
        data[self.DT_FMT] = {}
        rp = ComplexityReport(self.COMPLEXITY)
        line = rp.report_lines(self.DUMMY_PATH, data)
        assert line is None

    def test_simple_lines_no_previous(self):
        rp = ComplexityReport(self.COMPLEXITY)
        lines = rp.report_lines(self.DUMMY_PATH, self.COMPLEXITY[self.DUMMY_PATH])
        assert len(lines) == 2 + self.FILE_HEADER_LEN
        out = ' '.join(lines)
        assert out.count('(+0)') == 0

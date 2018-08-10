import copy

from tests import BaseTests

from decomplexator.report import ComplexityReport


class ReportTests(BaseTests):

    def test_file_header(self):
        fh = ComplexityReport.file_header(self.DUMMY_PATH)
        assert len(fh) == 3
        assert len(fh[1]) == len(fh[2])
        assert self.DUMMY_PATH in fh[1]

    def test_report_scores(self):
        rp = ComplexityReport(self.COMPLEXITY)
        assert rp.scores == self.COMPLEXITY

    def test_simple_report(self):
        rp = ComplexityReport(self.COMPLEXITY)
        data = rp.print_report(print_it=False)
        assert len(data) == len(self.COMPLEXITY[self.DUMMY_PATH][self.DT_FMT].keys()) + 1
        assert self.DUMMY_PATH in data[0]

    def test_calc_change_1st_run(self):
        node = 'fun1'
        cur = self.COMPLEXITY[self.DUMMY_PATH][self.DT_FMT][node]
        prev = None
        change = ComplexityReport.calc_changes(node, cur, prev)
        assert change.cognitive == 0
        assert change.cyclomatic == 0

    def test_calc_change_no_change(self):
        node = 'fun1'
        cur = self.COMPLEXITY[self.DUMMY_PATH][self.DT_FMT][node]
        prev = copy.deepcopy(cur)
        change = ComplexityReport.calc_changes(node, cur, prev)
        assert change.cognitive == 0
        assert change.cyclomatic == 0

    def test_calc_change(self):
        node = 'fun1'
        cur = self.COMPLEXITY[self.DUMMY_PATH][self.DT_FMT][node]
        prev = (1, 4, node)
        change = ComplexityReport.calc_changes(node, cur, prev)
        assert change.cognitive == cur[0] - prev[0]
        assert change.cyclomatic == cur[1] - cur[1]

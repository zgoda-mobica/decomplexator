from .utils import NodeComplexity, ComplexityChange


class ComplexityReport:

    FMT_SIMPLE = '{:>44} cyclomatic: {:>2}; cognitive: {:>2}'
    FMT_CONT = '{:>44} cyclomatic: {:>2} ({:+}); cognitive: {:>2} ({:+})'

    def __init__(self, scores):
        self.scores = scores

    def print_report(self, continuous=False, print_it=True):
        lines = []
        for filename, filedata in self.scores.items():
            if continuous:
                report_lines = self.continuous_report_lines(filename, filedata)
            else:
                report_lines = self.report_lines(filename, filedata)
            if report_lines:
                lines.extend(report_lines)
        if print_it:
            for line in lines:
                print(line)
        else:
            return lines

    @staticmethod
    def file_header(filename):
        return ['\n', filename, '=' * len(filename)]

    @staticmethod
    def calc_changes(node, cur, prev):
        if prev is None:
            return ComplexityChange(0, 0)
        missing = NodeComplexity(cognitive=0, cyclomatic=0, name='missing')
        cyclomatic_change = cur[node].cyclomatic - prev.get(node, missing).cyclomatic
        cognitive_change = cur[node].cognitive - prev.get(node, missing).cognitive
        return ComplexityChange(cognitive_change, cyclomatic_change)

    def continuous_report_lines(self, filename, filedata):
        available = sorted(filedata.keys())
        latest = filedata[available[-1]]
        previous = None
        if len(available) > 1:
            previous = filedata[available[-2]]
        node_names = sorted(latest.keys())
        if not node_names:
            return
        lines = self.file_header(filename)
        for node_name in node_names:
            change = self.calc_changes(node_name, latest, previous)
            line = self.FMT_CONT.\
                format(
                    node_name, latest[node_name].cyclomatic, change.cyclomatic,
                    latest[node_name].cognitive, change.cognitive
                )
            lines.append(line)
        return lines

    def report_lines(self, filename, filedata):
        available = sorted(filedata.keys())
        latest = filedata[available[-1]]
        node_names = sorted(latest.keys())
        if not node_names:
            return
        lines = self._file_header(filename)
        for node_name in node_names:
            line = self.FMT_SIMPLE.\
                format(node_name, latest[node_name].cyclomatic, latest[node_name].cognitive)
            lines.append(line)
        return lines

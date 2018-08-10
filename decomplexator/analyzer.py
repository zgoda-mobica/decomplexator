import ast
from datetime import datetime

from mccabe import PathGraphingAstVisitor
from .cc import CognitiveComplexity
from .utils import normalize_fname, NodeComplexity, load_previous_scores, save_scores


class ComplexityAnalyzer:

    """
    Python code complexity analyzer object that keeps complexity information for particular file.
    """

    def __init__(self, filename=None):
        self.cognitive = {}
        self.cyclomatic = {}
        self.filename = filename
        self._summary = None

    def analyze(self, filename=None):
        if filename is not None:
            self.filename = filename
        cognitive = CognitiveComplexity()
        self.cognitive = cognitive.evaluate(self.filename)
        self.cyclomatic = self._cyclomatic(self.filename)

    def has_data(self):
        return bool(self.cognitive and self.cyclomatic)

    def _cyclomatic(self, filename):
        with open(filename, 'r') as fp:
            code = fp.read()
        tree = compile(code, filename, 'exec', ast.PyCF_ONLY_AST)
        visitor = PathGraphingAstVisitor()
        visitor.preorder(tree, visitor)
        ret = {}
        for name, graph in visitor.graphs.items():
            ret[name] = graph.complexity()
        return ret

    def summary(self):
        if self._summary is not None:
            return self._summary
        key = datetime.utcnow().isoformat(timespec='seconds')
        nodes = set(self.cognitive.keys())
        nodes.update(self.cyclomatic.keys())
        ret = {
            self.filename: {
                key: {},
            }
        }
        for node in nodes:
            ret[self.filename][key][node] = NodeComplexity(
                cognitive=self.cognitive.get(node),
                cyclomatic=self.cyclomatic.get(node),
                name=node
            )
        self._summary = ret
        return ret

    def persist(self, filename=None):
        if not self.has_data():
            return
        data = self.summary()
        storage = load_previous_scores(filename)
        file_data = storage.setdefault(self.filename, data[self.filename])
        file_data.update(data[self.filename])
        save_scores(storage, filename)


class AnalyzerGroup:

    """
    Analyzers that are meant to be used together, eg. for files in the same project
    """

    def __init__(self, files=None):
        if files is None:
            files = []
        self.files = [normalize_fname(f) for f in files]
        self.analyzers = {}

    def add_files(self, files):
        self.files.extend([normalize_fname(f) for f in files])

    def analyze(self):
        for fn in self.files:
            analyzer = ComplexityAnalyzer(fn)
            analyzer.analyze()
            self.analyzers[fn] = analyzer

    def summary(self):
        data = {}
        for _, analyzer in self.analyzers.items():
            data.update(analyzer.summary())
        return data

    def persist(self, filename=None):
        storage = load_previous_scores(filename)
        for python_fname in self.files:
            an = self.analyzers[python_fname]
            if an.has_data():
                data = an.summary()
                file_data = storage.setdefault(python_fname, data[python_fname])
                file_data.update(data[python_fname])
        save_scores(storage, filename)

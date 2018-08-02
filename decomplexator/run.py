import glob
from os import path
import argparse

from .analyzer import AnalyzerGroup
from .report import ComplexityReport
from .utils import clear_storage, load_previous_scores


def make_parser():
    parser = argparse.ArgumentParser(
        description='Python code complexity analyzer',
    )
    parser.add_argument(
        '-i', '--input-file', dest='filename',
        help='Python file to analyze',
    )
    parser.add_argument(
        '-d', '--directory', dest='project_dir',
        help='directory to analyze',
    )
    parser.add_argument(
        '-c', '--continuous', action='store_true',
        help='compare current results with previous and store for future runs',
    )
    parser.add_argument(
        '--clear', action='store_true',
        help='clean stored results',
    )
    return parser


def analyze_file(fname, continuous):
    return _analyze_files([fname], continuous)


def _analyze_files(filenames, continuous):
    group = AnalyzerGroup(filenames)
    group.analyze()
    summary = group.summary()
    if continuous:
        group.persist()
    return summary


def analyze_directory(dirname, continuous):
    dir_path = path.abspath(path.join(dirname, '**', '*.py'))
    files = [path.join(dirname, fn) for fn in glob.iglob(dir_path, recursive=True)]
    return _analyze_files(files, continuous)


def print_report(scores, continuous):
    if continuous:
        data = load_previous_scores()
        for k, v in scores.items():
            v.update(data.get(k, {}))
    report = ComplexityReport(scores)
    report.print_report(continuous)


def main():
    parser = make_parser()
    args = parser.parse_args()
    if args.clear:
        clear_storage()
    else:
        if not args.filename and not args.project_dir:
            parser.print_usage()
            raise SystemExit(1)
        if args.filename:
            scores = analyze_file(args.filename, args.continuous)
        else:
            scores = analyze_directory(args.project_dir, args.continuous)
        print_report(scores, args.continuous)

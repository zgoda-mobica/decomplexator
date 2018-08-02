import os
from os import path
import pickle
from collections import namedtuple, Mapping

import xdg


STORAGE_FNAME = 'cog.pickle'


NodeComplexity = namedtuple('NodeComplexity', ['cognitive', 'cyclomatic', 'name'])
ComplexityChange = namedtuple('ComplexityChange', ['cognitive', 'cyclomatic'])


def get_storage_path(filename=None):
    if filename is None:
        filename = STORAGE_FNAME
    storage_dir = xdg.XDG_DATA_HOME
    return normalize_fname(path.join(storage_dir, filename))


def normalize_fname(fn):
    """Normalize file name to absolute clean path"""
    return path.normpath(path.abspath(fn))


def clear_storage(filename=None):
    os.remove(get_storage_path(filename))


def load_previous_scores(filename=None):
    try:
        with open(get_storage_path(filename), 'r+b') as fp:
            data = pickle.load(fp)
        if not isinstance(data, Mapping):
            data = {}
    except (FileNotFoundError, EOFError, pickle.UnpicklingError):
        data = {}
    return data


def save_scores(data, filename=None):
    filename = get_storage_path(filename)
    os.makedirs(path.dirname(filename), exist_ok=True)
    with open(filename, 'w+b') as fp:
        pickle.dump(data, fp)

import os
from os.path import dirname, join, abspath
import sys


def _intialization():
    sys.path.insert(0, abspath(
        join(os.path.dirname(os.path.abspath("__file__")), '..')))

import sys
from os.path import dirname
sys.path.append(dirname(dirname(__file__)))


from script.util import bootstrap, run_test

env, registry, settings = bootstrap('testing.ini')

run_test(settings, cucumber=True, behave=True)

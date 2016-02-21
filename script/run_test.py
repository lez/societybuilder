from script.util import bootstrap, run_test
import sys

env, registry, settings = bootstrap('testing.ini')

run_test(settings)

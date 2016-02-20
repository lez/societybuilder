from script.util import bootstrap, run_test
import sys

if len(sys.argv) == 1:
    sys.argv.append('testing.ini')
if sys.argv[1] != 'testing.ini':
    print('invalid config file for testing:', sys.argv[1])

env, registry, settings = bootstrap()

run_test(settings)

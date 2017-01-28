import sys
from os.path import dirname
sys.path.append(dirname(dirname(__file__)))


from script.util import bootstrap, run_test

env, registry, settings = bootstrap(sys.argv[1])

from sb.model.type import User, Page

from sb.util import permalink

# Iterate over the pages and fill in their permalink field

for p in Page.select():

    p.permalink_lower = p.permalink.lower()
    p.save()

    print(p.permalink, p.permalink_lower)

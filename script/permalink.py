import sys
from os.path import dirname
sys.path.append(dirname(dirname(__file__)))


from script.util import bootstrap, run_test

env, registry, settings = bootstrap(sys.argv[1])

from ist.model.type import Page

from ist.util import permalink

# Iterate over the pages and fill in their permalink field

for p in Page.select():

    p.permalink = permalink(p.name)
    p.save()

    print(p.name, p.permalink)

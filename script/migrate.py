import sys
from os.path import dirname
sys.path.append(dirname(dirname(__file__)))


from script.util import bootstrap, run_test

env, registry, settings = bootstrap(sys.argv[1])

from ist.model.type import User

from ist.util import permalink

# Iterate over the pages and fill in their permalink field

for u in User.select():

    u.login_lower = u.login.lower()
    u.save()

    print(u.login, u.login_lower)

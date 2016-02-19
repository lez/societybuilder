from script.util import bootstrap, reset_db

env, registry, settings = bootstrap()

reset_db(settings)

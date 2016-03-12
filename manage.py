# manage.py

from collections import OrderedDict
import os
import unittest
import coverage

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from pandas.compat import u
from flask import g

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/server/config.py',
        'project/server/*/__init__.py'
    ]
)
COV.start()

from project.server import app, db

import pandas as pd

migrate = Migrate(app)
manager = Manager(app)




if __name__ == '__main__':
    manager.run()

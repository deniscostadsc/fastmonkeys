#!/usr/bin/env python

from fastmonkeys import app
from fastmonkeys.database import init_db

init_db()

app.run(debug=True)

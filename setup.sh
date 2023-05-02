#!/bin/bash

python -mpip install --user -r <(/usr/local/py-utils/bin/poetry export --with dev)
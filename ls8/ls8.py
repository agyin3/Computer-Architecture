#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

data = sys.argv[1]

cpu = CPU()

cpu.load(data)
cpu.run()

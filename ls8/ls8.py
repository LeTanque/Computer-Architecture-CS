#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

# cpu = CPU()

# cpu.load()
# cpu.run()

if sys.argv[1]:
    cpu = CPU(sys.argv[1])

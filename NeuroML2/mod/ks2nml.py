#!/usr/bin/env python3
"""
Script to convert KS activation equations to NML for insertion into a
channel.nml file

File: NeuroML2/mod/ks2nml.py

Copyright 2024 Ankur Sinha
Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com>
"""


import textwrap
import re


src_str = """
    ~ C0 <-> C1      (c01,c10)
    ~ C1 <-> C2      (c12,c21)
    ~ C2 <-> C3      (c23,c32)
    ~ C3 <-> C4      (c34,c43)
    ~ O0 <-> O1      (o01,o10)
    ~ O1 <-> O2      (o12,o21)
    ~ O2 <-> O3      (o23,o32)
    ~ O3 <-> O4      (o34,o43)
    ~ C0 <-> O0      (f0,b0)
    ~ C1 <-> O1      (f1,b1)
    ~ C2 <-> O2      (f2,b2)
    ~ C3 <-> O3      (f3,b3)
    ~ C4 <-> O4      (f4,b4)
"""

regex = re.compile("\s*~\s+(\S+)\s+<->\s+(\S+)\s+\((\S+),(\S+)\)")
src = textwrap.dedent(src_str)
for line in src.splitlines():
    matched = regex.match(line)
    if matched:
        src_state = matched.group(1)
        dest_state = matched.group(2)
        fwd_rate = matched.group(3)
        rev_rate = matched.group(4)
        print(f"""
            <forwardTransition id="{fwd_rate}" from="{src_state}" to="{dest_state}" >
                <rate type="" />
            </forwardTransition>
            <reverseTransition id="{rev_rate}" from="{src_state}" to="{dest_state}" >
                <rate type="" />
            </reverseTransition>
        """)

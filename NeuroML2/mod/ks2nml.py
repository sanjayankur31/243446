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
    ~ C1 <-> C2                 (f01,b01)
    ~ C2 <-> C3                 (f02,b02)
    ~ C3 <-> C4                 (f03,b03)
    ~ C4 <-> C5                 (f04,b04)
    ~ C5 <-> O                  (f0O,b0O)
    ~ O <-> B                   (fip,bip)
    ~ O <-> I6                  (fin,bin)
    ~ I1 <-> I2                 (f11,b11)
    ~ I2 <-> I3                 (f12,b12)
    ~ I3 <-> I4                 (f13,b13)
    ~ I4 <-> I5                 (f14,b14)
    ~ I5 <-> I6                 (f1n,b1n)
    ~ C1 <-> I1                 (fi1,bi1)
    ~ C2 <-> I2                 (fi2,bi2)
    ~ C3 <-> I3                 (fi3,bi3)
    ~ C4 <-> I4                 (fi4,bi4)
    ~ C5 <-> I5                 (fi5,bi5)
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

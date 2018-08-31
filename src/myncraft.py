#!/usr/bin/env python
# # python 2 compatibility
# try: input = raw_input
# except NameError: pass

import os
from mcrcon import MCRcon

#with MCRcon(os.environ['MC_SERVER'], os.environ['MC_PASSWORD']) as mcr:
with MCRcon(os.environ['MC_SERVER'], os.environ['MC_PASSWORD']) as mcr:
      resp = mcr.command("/list")
      print(resp)

#!/usr/bin/env python3

import sys, json;
data = json.load(sys.stdin)
print(json.dumps(data, indent=4))

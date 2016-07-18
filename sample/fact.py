def fact (x):
  if x<=1:
    return 1
  else:
    return x*fact(x-1)

import sys
print fact(int(sys.argv[1]))

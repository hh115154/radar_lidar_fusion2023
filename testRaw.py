#!/usr/bin/env python

import time

t1 = time.time()
file1 = open('test2.txt', 'a')
for i in range(15000000):
    print >> file1, 'AAAAAAAA'
file1.close()
print(time.time() - t1)
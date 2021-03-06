Bitwise Operations
------------------

Math ops that work 1 bit at a time in a number.

A  B   A  &  B    (& is bitwise AND)
----------------
0  0      0
0  1      0
1  0      0
1  1      1

A  B   A  |  B    (| is bitwise OR)
----------------
0  0      0
0  1      1
1  0      1
1  1      1

A  B   A  ^  B    (^ is bitwise XOR, "exclusive OR")
----------------
0  0      0
0  1      1
1  0      1
1  1      0

A   ~A  (~ is bitwise NOT)
-------
0   1
1   0

  0b01010101
& 0b11100011
------------
  0b01000001 == 64

In general:

OR can be used to set bits to 1
AND can be used to clear bits to 0

      vv
  0b111001
& 0b110011  "AND mask"--stencil
----------
  0b110001
      ^^

      vv
  0b111001
| 0b001100  Use OR to force these two bits to 1 in the output
----------
  0b111101
      ^^

Bit shifting
------------

  111001  >> shift right
  011100  << shift left
  001110
  000111
  000011
  000001
  000000


123456 >>
012345
001234
000123
000012
000001
000000


      123456 <<
     1234560 <<
    12345600 <<
   123456000 <<





 vv
12345 -> [do some stuff] -> 23
.MM..
02300
00230
00023
   ^^

To extract individual numbers from inside a value, mask and shift.
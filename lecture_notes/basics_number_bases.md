Number Bases
------------

It's the "language" that a number is written down in.

Base 2: binary
Base 8: octal (rarely used)
Base 10: decimal (what we know from grade school, regular boring ol numbers)
Base 16: hexadecimal, "hex"
Base 64: base 64 (no special name...sad face.)

base 10 (decimal)

+-----1000's place 10^3
|+----100's place 10^2
||+---10's place 10^1
|||+--1's place 10^0
||||
abcd

1234
1 2 3 4:

1 1000
2 100s
3 10s
4 1s

1234 == 1 * 1000 + 2 * 100 + 3 * 10 + 4 * 1
        ^          ^         ^        ^
This mathematical breakdown works in EVERY number base; only difference, the places have different values.

base 2 (binary)
+-----8's place 2^3
|+----4's place 2^2
||+---2's place 2^1
|||+--1's place 2^0
||||
abcd

0011 binary
0011 binary == 0 * 8 + 0 * 4 + 1 * 2 + 1 * 1 = 3 decimal

You can put as many leading decimals as you want.

binary digits ("bit")

8 bits == "byte"
4 bits = "nybble"
Thus: 2 "nybbles" == 1 "byte"
"Kilobyte" is actually 1024 "bytes" even though "kilo" technically means 1000.
MB = Megabytes
Mb = Megabits

Number base matters when you write it down:
11000 can be 24 (binary) or 11,000 (decimal)
11000 binary = 24 decimal
11000 decimal = 11,000 decimal

Python Prefix
-------------
[none] = decimal
0b =     binary
0x =     hex
0o =     octal

11000 = 11,000 decimal
0b11000 = 24 binary
0x11000 = 69632 decimal
0o11000 = 4608 decimal


#ff12D9
#ffff00 == yellow
(255, 255, 0) == yellow
(11111111, 11111111, 00000000) == yellow

red      green    blue
ff       ff       00       hex
255      255      0        decimal
11111111 11111111 00000000 binary
|      | |      | |      |
-------- -------- --------
  byte     byte     byte

Lower the base, the more digits required to represent the value.
ff == 2 digits, base 16
255 == 3 digits, base 10
11111111 == 8 digits, base 2

1 hex digits == 4 bits (binary digits)

0000 0  ----> 1 nybble binary, 1 digit hex
0001 1 
0010 2
0011 3
0100 4
0101 5
0110 6 
0111 7
1000 8
1001 9
1010 A
1011 B
1100 C
1101 D
1110 E
1111 F

00101010
Convert?
0010    1010
  2       A
0b00101010 == 0x2A
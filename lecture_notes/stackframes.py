"""
Stack Frames
-------------
Stack grows downwards

When you call:
    Allocate a stack frame
        Stack frame is the return address and the locals

When you return:
    Deallocate (pop) that stack frame

return value: 14

"""

def mult2(x, y):
    z = x * y

    x = 999

    return z

def main():
    a = 2

    # addr_1
    # v
    b = mult2(a, 7)

    print(b)  # 14

    return #

main()

print("Done!")  # addr_2 # <-- PC
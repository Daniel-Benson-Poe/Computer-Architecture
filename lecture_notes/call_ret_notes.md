CALL and RET
-------------

Subroutines
    Functions, but you can't pass anything in
    And they can't return anything

Example:
def foo():
    print("foo 1")
    return

def bar():
    print("bar 1")
    foo()
    print("bar 2")  # addr_2

    return

print("main 1")
bar()
print("main 2")  # addr_1

stack: addr_1 addr_2 <- top

CALL:
    push return address on stack
    set pc to address of subroutine

RET
    pop return addr off top of stack
    set pc to the return address
import microcontrol

from functions import *

@microcontrol.io("J6")
def io_a0():
    return False

@microcontrol.io("H5")
def io_a1():
    return False

@microcontrol.io("H6")
def io_a2():
    return False

@microcontrol.io("G4")
def io_a3():
    return False

@microcontrol.io("H7")
def io_b0():
    return False

@microcontrol.io("E3")
def io_b1():
    return False

@microcontrol.io("E4")
def io_b2():
    return False

@microcontrol.io("D2")
def io_b3():
    return False

@microcontrol.io("G5")
def io_r0():
    return False

@microcontrol.io("J1")
def io_s0():
    return False

@microcontrol.io("J2")
def io_s1():
    return False

@microcontrol.io("J3")
def io_s2():
    return False

@microcontrol.io("H1")
def io_s3():
    return False

@microcontrol.io("F2")
def io_r3():
    return False

@microcontrol.io("A13")
def io_d0():
    return False

@microcontrol.io("B13")
def io_d1():
    return False

@microcontrol.io("C13")
def io_d2():
    return False

@microcontrol.io("A14")
def io_d3():
    return False

@microcontrol.io("B14")
def io_d4():
    return False

@microcontrol.io("E14")
def io_d5():
    return False

@microcontrol.io("A15")
def io_d6():
    return False

@microcontrol.io("B15")
def io_d7():
    return False

@microcontrol.io("E11")
def io_d8():
    return False

@microcontrol.io("F11")
def io_d9():
    return False

@microcontrol.io("H12")
def io_d10():
    return False

@microcontrol.io("H13")
def io_d11():
    return False

@microcontrol.io("G12")
def io_d12():
    return False

@microcontrol.io("F12")
def io_d13():
    return False

@microcontrol.io("F13")
def io_d14():
    return False

@microcontrol.io("D13")
def io_d15():
    return False

@microcontrol.macro
def demi_add(a1, b1, r0):
    s1 = xor(r0, xor(a1, b1))
    r1 = or2(and2(r0, xor(a1, b1)), and2(a1, b1))
    return s1, r1

@microcontrol.macro
def add(a0, a1, a2, a3, b0, b1, b2, b3, r):
    s0, r0 = demi_add(a0, b0, r)
    s1, r1 = demi_add(a1, b1, r0)
    s2, r2 = demi_add(a2, b2, r1)
    s3, r3 = demi_add(a3, b3, r2)
    
    return s0, s1, s2, s3, r3

@microcontrol.macro
def segments(a, b, c, d):

    s0 = or4(b, d, and2(a,c), and2(no(a),no(c)))
    s1 = or4(and2(no(b), no(a)), d, and2(c, no(a)), and2(no(b), c))
    s2 = or2(no(c), no(xor(a, b)))
    s3 = or3(d, and2(no(a), b), xor(b, c))
    s4 = and2(no(a), or2(b, no(c)))
    s5 = or3(a, no(b), c)
    s6 = or4(d, and2(b, or2(no(c), no(a))), and2(no(c), no(a)), and3(a, no(b), c))

    return s0, s1, s2, s3, s4, s5, s6

@microcontrol.macro
def divide_segments(s0, s1, s2, s3, s4):
    
    f3 = 0
    f2 = 0
    f1 = and2(s4, or2(s2, s3))
    f0 = or2(and2(s3, or2(and2(s1, s2), and2(no(s4), or2(s1, s2)))), and2(s4, no(or2(s3, s2))))

    g3 = or2(and3(s3, no(s1,), no(xor(s4, s2))), and3(s4, s1, no(or2(s3, s2))))
    g2 = or2(and3(no(s4), s2, or2(s1, no(s3))), and3(s4, no(s2), or2(s3, no(s1))))
    g1 = or3(and3(s4, no(s2), no(xor(s3, s1))), and2(no(s4), or2(and2(no(s3), s1), and3(s3, s2, no(s1)))), and3(no(s3), s2, s1))
    g0 = s0

    return f0, f1, f2, f3, g0, g1, g2, g3

@microcontrol.macro
def pass_numbers(n0, n1, n2, n3, v):

    s0 = and2(n0, v)
    s1 = and2(n1, v)
    s2 = and2(n2, v)
    s3 = and2(n3, v)

    return s0, s1, s2, s3

@microcontrol.macro
def multiply(a0, a1, a2, a3, b0, b1, b2, b3):

    s0, t1, t2, t3 = pass_numbers(a0, a1, a2, a3, b0)
    s1, t2, t3, t4, t5 = add(*pass_numbers(a0, a1, a2, a3, b1), t1, t2, t3, 0, 0)
    s2, t3, t4, t5, t6 = add(*pass_numbers(a0, a1, a2, a3, b2), t2, t3, t4, t5, 0)
    s3, t4, t5, t6, t7 = add(*pass_numbers(a0, a1, a2, a3, b3), t3, t4, t5, t6, 0)

    return s0, s1, s2, s3, t4

@microcontrol.process
def process1():

    a0 = io_a0()
    a1 = io_a1()
    a2 = io_a2()
    a3 = io_a3()

    b0 = io_b0()
    b1 = io_b1()
    b2 = io_b2()
    b3 = io_b3()

    r = io_r0()

    s0, s1, s2, s3, r3 = multiply(a0, a1, a2, a3, b0, b1, b2, b3)

    f0, f1, f2, f3, g0, g1, g2, g3 = divide_segments(s0, s1, s2, s3, r3)

    n0, n1, n2, n3, n4, n5, n6 = segments(f0, f1, f2, f3)
    o0, o1, o2, o3, o4, o5, o6 = segments(g0, g1, g2, g3)

    io_d0.set(n0)
    io_d1.set(n1)
    io_d2.set(n2)
    io_d3.set(n3)
    io_d4.set(n4)
    io_d5.set(n5)
    io_d6.set(n6)

    io_d8.set(o0)
    io_d9.set(o1)
    io_d10.set(o2)
    io_d11.set(o3)
    io_d12.set(o4)
    io_d13.set(o5)
    io_d14.set(o6)

microcontrol.config = ["pink", "blue", True]

microcontrol.start()
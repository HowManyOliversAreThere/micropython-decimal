import sys
import random
from mpy_decimal.mpy_decimal import *

# Imports modules and it sets limits depending on the implementation
if sys.implementation.name == "cpython":
    import traceback
    import time
    iteration_limit: int = 100000
    pi_decimals: int = 5000
if sys.implementation.name == "micropython":
    import machine
    import utime
    iteration_limit: int = 1000
    pi_decimals: int = 300

line: str = '+' + ('-' * 63) + '+'


def system_machine_info() -> None:
    """It prints system information."""
    print("{:<30}".format("Implementation name:"), sys.implementation.name)
    print("{:<30}".format("Implementation version:"),
          "{0}.{1}.{2}".format(
        sys.implementation.version[0],
        sys.implementation.version[1],
        sys.implementation.version[2]
    )
    )
    print("{:<30}".format("Implementation platform:"), sys.platform)
    if sys.implementation.name == "micropython":
        print("{:<30}".format("CPU frequency:"),
              machine.freq() // 1000000, "Mhz")


def get_time_ms() -> int:
    """It gets the time in miliseconds.
    The way to get it depends on the implementation."""
    if sys.implementation.name == "cpython":
        return round(time.time() * 1000)
    if sys.implementation.name == "micropython":
        return utime.ticks_ms()


def gen_random_number() -> DecimalNumber:
    """Generates a random number with a number of decimals equal to scale.
    The number of digits for the integer part is between scale/2 and scale.
    It can be either positive or negative.
    abs(gen_random_number()) can be used for postive numbers only.
    """
    n: int = 0
    length: int = DecimalNumber.get_scale(
    ) + random.randrange(DecimalNumber.get_scale() // 2, DecimalNumber.get_scale())
    for _ in range(0, length):
        n = n * 10 + random.randrange(0, 9)
    if random.randrange(0, 2) == 0:
        n = -n
    return DecimalNumber(n, DecimalNumber.get_scale())


def perf_decimal_number() -> None:
    """Performance calculations of DecimalNumber class"""
    print("{:<30}".format("Scale (max. decimals):"), DecimalNumber.get_scale())
    print("{:<30}".format("Iterations per test:"), iteration_limit)

    n1 = gen_random_number()
    zero: bool = True
    while zero:
        n2 = gen_random_number()
        zero = (n2 == DecimalNumber(0))
    print("{:<30}".format("Number 1:"), n1)
    print("{:<30}".format("Number 2:"), n2)

    # Addition
    t = get_time_ms()
    for _ in range(0, iteration_limit):
        n3 = n1 + n2
    t = get_time_ms() - t
    print("{:<30}".format("Addition (n1 + n2):"), t / iteration_limit, "ms")

    # Subtraction
    t = get_time_ms()
    for _ in range(0, iteration_limit):
        n3 = n1 - n2
    t = get_time_ms() - t
    print("{:<30}".format("Subtraction (n1 - n2):"), t / iteration_limit, "ms")

    # Multiplication
    t = get_time_ms()
    for _ in range(0, iteration_limit):
        n3 = n1 * n2
    t = get_time_ms() - t
    print("{:<30}".format("Multiplication (n1 * n2):"),
          t / iteration_limit, "ms")

    # Division
    t = get_time_ms()
    for _ in range(0, iteration_limit):
        n3 = n1 / n2
    t = get_time_ms() - t
    print("{:<30}".format("Division (n1 / n2):"), t / iteration_limit, "ms")

    # Square root
    n = abs(n1)
    t = get_time_ms()
    for _ in range(0, iteration_limit):
        n3 = n.square_root()
    t = get_time_ms() - t
    print("{:<30}".format("Square root abs(n1):"), t / iteration_limit, "ms")

    # Power
    n = DecimalNumber.from_string("1.01234567")
    e: int = 15
    t = get_time_ms()
    for _ in range(0, iteration_limit):
        n3 = n ** e
    t = get_time_ms() - t
    print("{:<30}".format("Power: 1.01234567 ** 15"), t / iteration_limit, "ms")

    # Creation from integer
    n = n1._number
    d = n1._num_decimals
    t = get_time_ms()
    for _ in range(0, iteration_limit):
        n3 = DecimalNumber(n, d)
    t = get_time_ms() - t
    print("{:<30}".format("DecimalNumber from int:"), t / iteration_limit, "ms")

    # Creation from string
    n = str(n1)
    t = get_time_ms()
    for _ in range(0, iteration_limit):
        n3 = DecimalNumber.from_string(n)
    t = get_time_ms() - t
    print("{:<30}".format("DecimalNumber from string:"),
          t / iteration_limit, "ms")


def perf_decimal_number_pi() -> None:
    """Performance of the calculation of PI."""
    # Calculating PI
    # PI is precalculated up to 100 decimals.
    # We need to set scale > 100 to actually calculated.
    current_scale = DecimalNumber.get_scale()
    DecimalNumber.set_scale(pi_decimals)
    t = get_time_ms()
    pi = DecimalNumber.pi()
    t = get_time_ms() - t
    print("{:<30}".format("Pi with " + str(pi_decimals) + " decimals:"), t/1000, "s")
    print(pi)
    DecimalNumber.set_scale(current_scale)


def print_title(title: str) -> None:
    """Auxiliary function to print a title."""
    print("")
    print(line)
    print("|  " + "{:<59}".format(title) + "  |")
    print(line)


print_title("SYSTEM INFORMATION")
system_machine_info()
print_title("PERFORMANCE OF DecimalNumber")
perf_decimal_number()
print_title("CALCULATING PI")
perf_decimal_number_pi()

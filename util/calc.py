def gcd(a, b):
    """
    gcd function

    :type a: int
    :type b: int
    rtype: int
    """
    while b != 0:
        a, b = b, a % b
    return a


def lcm(a, b):
    """
    lcm function using gcd()

    :type a: int
    :type b: int
    rtype: int
    """
    return (a * b) // gcd(a, b)

def gcd(*args):
    """
    gcd function that can handle multiple args
    """
    # if input has less than two args
    if len(args) < 2:
        raise Exception('Not enough arguments')

    def euclid_algorithm(a, b):
        while b != 0:
            a, b = b, a % b
        return a

    ans = euclid_algorithm(args[0], args[1])
    for i in range(2, len(args)):
        ans = euclid_algorithm(ans, args[i])

    return ans


def lcm(*args):
    """
    lcm function that can handle multiple args
    """
    # if input has less than two args
    if len(args) < 2:
        raise Exception('Not enough arguments')

    product = 1
    for i in range(len(args)):
        product *= args[i]

    ans = 1
    for i in range(len(args)):
        ans = ans * args[i] // gcd(ans, args[i])

    return ans

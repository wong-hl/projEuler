import numpy as np
import math
class TestBases(object):
    def __init__(self, test_number):
        self.which_base = None

        self.map_val_to_base = self.create_hash_map()

        self.initialise(test_number)

    def create_hash_map(self):
        return {1: np.asarray([2]),
                2: np.asarray([2,3]),
                3: np.asarray([31,73]),
                4: np.asarray([2,3,5]),
                5: np.asarray([2,3,5,7]),
                6: np.asarray([2,7, 61]),
                7: np.asarray([2,13, 23, 1662803]),
                8: np.asarray([2,3,5,7,11]),
                9: np.asarray([2,3,5,7,11,13]),
                10: np.asarray([2,3,5,7,11,13,17]),
                }

    def get_hash_category(self, test_number):
        if test_number < 2047:
            return 1
        elif test_number < 1373653:
            return 2
        elif test_number < 9080191:
            return 3
        elif test_number < 25326001:
            return 4
        elif test_number < 3215031751:
            return 5
        elif test_number < 4759123141:
            return 6
        elif test_number < 1122004669633:
            return 7
        elif test_number < 2152302898747:
            return 8
        elif test_number < 3474749660383:
            return 9
        elif test_number < 341550071728321:
            return 10
        else:
            raise ValueError("Test number exceeds range of validity")

    def determine_test_base(self, test_number):
        which_category = self.get_hash_category(test_number)
        self.which_base = self.map_val_to_base[which_category]

    def initialise(self, test_number):
        self.determine_test_base(test_number)

    def get_base(self):
        return self.which_base

def factorise_power2_out(test_number):

    r = (test_number).bit_length() - 1 

    while True:
        two_to_r = (1 << r) 
        d = (test_number - 1) // two_to_r

        if two_to_r*d == test_number - 1:
            return r, d
        else:
            r -= 1

    # # print("r = {} d = {} 2^r*d = {}".format(r, d, two_to_r*d))

    # while two_to_r*d != test_number -1:
    #     r -= 1
    #     two_to_r = (1 << r) 
    #     d = (test_number - 1) // (1 << r) 

    #     # print("r = {} d = {}".format(r, d))

    # return r, d


def is_prime_miller_test(test_number):

    if test_number == 2:
        return True
    elif test_number & 1 == 0:
        return False

    r, d = factorise_power2_out(test_number)

    # print("r = {} d = {}".format(r, d))

    bases = TestBases(test_number)
    test_bases = bases.get_base()

    for a in test_bases:

        if 1 < math.gcd(a, test_number) < test_number:
            return False

        # x = (a ** d) % test_number
        # print("{}".format(x))

        # if x == 1 or x == test_number - 1:
        #     continue
        
        # for _ in range(r-1):
        #     x = x*x % test_number

        #     if x == test_number - 1:
        #         continue
        #     else:
        #         break

        # return False

        if miller_inner(a, test_number, d, r) == False:
            return False

    return True

def miller_inner(witness, test_number, d, r):
    x = (witness ** d) % test_number
    # print("{}".format(x))

    if x == 1 or x == test_number - 1:
        return
    
    for _ in range(r-1):
        x = x*x % test_number

        if x == test_number - 1:
            return

    return False



if __name__ == "__main__":
    # base = TestBases()
    # base.initialise(5555)

    # print("{}".format(base.get_base()))

    oeis_primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,
        61,67,71,73,79,83,89,97,101,103,107,109,113,127,
        131,137,139,149,151,157,163,167,173,179,181,191,
        193,197,199,211,223,227,229,233,239,241,251,257,
        263,269,271]

    my_primes = []

    for i in range(2, 300):
        if is_prime_miller_test(i):
            my_primes.append(i)
            print("i = {} is prime ".format(i, ))
        # print("")

    for prime in my_primes:
        if prime not in oeis_primes:
            print("{} identified as prime but isn't".format(prime))

    for prime in oeis_primes:
        if prime not in my_primes:
            print("{} is prime but not identified".format(prime))
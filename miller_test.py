import numpy as np
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

    if test_number & 1 == 0 and test_number != 2:
        return False

    r, d = factorise_power2_out(test_number)

    print("r = {} d = {}".format(r, d))

    bases = TestBases(test_number)
    test_bases = bases.get_base()

    for a in test_bases:
        x = (a ** d) % test_number
        print("{}".format(x))

        if x == 1 or x == test_number - 1:
            continue
        
        for _ in range(r-1):
            x = x*x % test_number

            if x == test_number - 1:
                continue
            else:
                break

        return False

    return True



if __name__ == "__main__":
    # base = TestBases()
    # base.initialise(5555)

    # print("{}".format(base.get_base()))

    for i in range(3, 20, 2):
        print("i = {} is prime = {}".format(i, is_prime_miller_test(i)))
        print("")
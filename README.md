# projEuler
Using Poject Euler problems to get to grips with Rust

In the table belows, the problems have been listed in order of completion and not by the problem number.

| Problem Number | Title                       | Solved? | Is solution brute force? | Additional Notes                                                                                                                                                                  |
|----------------|-----------------------------|:---------:|:--------------------------:|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|        1       |     Multiples of 3 and 5    |   Yes   |            No            |                                                                           Used sum of arithmetic series                                                                           |
|        2       |    Even Fibonacci Numbers   |   Yes   |            No            |                                           Used properties of addition to determine if even but still needs to find all Fibonacci numbers                                          |
|        3       |     Largest Prime Factor    |   Yes   |  No but could be better  |                                                           Combined Fermat factorisation method and Seive of Eratosthenes                                                          |
|        4       |  Largest Palindrome Product |   Yes   |            No            |                                                Factorised 3-digit number, made some assumptions then enforced palindrome criterion                                                |
|        5       |      Smallest Multiple      |   Yes   |            No            |                                                                     Used simple logic to check systematically                                                                     |
|        6       |    Sum Square Difference    |   Yes   |            No            |                                                             Used properties of series and algebra to make a one liner                                                             |
|        7       |        10001st Prime        |   Yes   |            No            |                                                      Used Seive of Eratosthenes and prime number theory to make initial guess                                                     |
|        8       | Largest Product in a Series |   Yes   |            Yes           |                                                                                                                                                                                   |
|        9       | Special Pythagorean Triplet |   Yes   |            No            |                                                Used simultaneous equations to simplify relation and test if criterion is fulfilled                                                |
|       10       |     Summation of Primes     |   Yes   |          Maybe?          |                                                                     Used Seive of Eratosthenes and dot product                                                                    |
|       16       |       Power Digit Sum       |   Yes   |            NO!           | 2^1000 is never directly computed. Decomposed large exponent into multiplication of smaller exponents, used bit shift to find 2^n, acyclic convolution, properties of multiplication and properties of sum of digits |
|       66       |     Diophantine Equation    |   Yes   | Well, I still needed to solve all equations less than 1000? So, Yes?| Originally intended to determine if there was a way to know the periodicity of sqrt(d) as a continued fraction to determine the length. This would be an indication of which convergent value corresponds to the fundamental solution. However, I am unable to find a reliable method in literature. I thought it might be related to if d is congruent to modulo 4?|
|       76       |     Counting Summations     |         |                          |                                                                                                                                                                                   |

# Project Euler
Using Poject Euler problems to get to grips with Rust

In the table belows, the problems have been listed in order of completion and not by the problem number.

| Problem Number | Title                       | Solved? | Is solution brute force? | Additional Notes                                                                                                                                                                  |
|:--------------:|:---------------------------:|:---------:|:--------------------------:|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
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
|       16       |       Power Digit Sum       |   Yes   |            NO!           | 2^1000 is never directly computed. Decomposed large exponent into multiplication of smaller exponents, used bit shift to find 2^n, acyclic convolution, decomposed multiplication into addition and properties of sum of digits |
|       66       |     Diophantine Equation    |   Yes   | Well, I still needed to solve all equations less than 1000? So, Yes?| Originally intended to determine if there was a way to know the periodicity of sqrt(d) as a continued fraction to determine the length. This would be an indication of which convergent value corresponds to the fundamental solution. However, I am unable to find a reliable method in literature. I thought it might be related to if d is congruent to modulo 4?|
| 75 | Singular Integer Right Triangles | Yes | No | Used the Euclid's formula to find the Pythagorean Triplets. Exploited 1) the fact that all coprime pairs lie on three branches to find m and n 2) all perimeters (sum of a, b, c) are even 3) the perimeter can be expressed in terms of m and n so a, b and c never need to be found 4) only found the primitive triplets as the rest are a multiple of it |
|       76       |     Counting Summations     |  Yes   |           Maybe?           | Utilised Euler's Pentagonal Theorem to obtain the partition recurrence relation. Cached prior solutions to solve solution in approx. 500ms.|
|78|Coin Partitions|  Yes   | No | Used formulation from 76. But, 1) used a vector to store previous values, and 2) only the significant decimal digits required in the modulo are stored. If the full number is stored, there will be overflow and exceed capacity of an i32.|
|77|     Prime Summations     |WIP| | |
|96|Su Doku|WIP| | |

In accordance to the rules of sharing solutions outside Project Euler - solutions to problems outside the first 100 should not be made outside the Project Euler discussion forum - the code for solving those problems are in a private repo. The table below details which those problems were solved and that exists within a private repo. 

| Problem Number | Title | Solved? | Is solution brute force? | Time Taken | Additional Comments |
|-|-|:-:|:-:|:-:|-|
| 760 | Sum Over Bitwise Operations | In Progress | - | -  | - |
|  |  |  |  |  |  |

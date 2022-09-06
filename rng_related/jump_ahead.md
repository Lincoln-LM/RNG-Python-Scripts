# GF(2)-linear RNG Jump Ahead

## Intro
This document serves to explain how the math behind jump ahead works, along with example code for how this could be implemented.

A lot of the explanation of the math is repeating what is described in “Efficient Jump Ahead for F2-Linear Random Number Generators” in a way that is easier for my brain to understand.

## Matrix Representation of PRNG

The sequence of the states of GF(2)-linear PRNGs can be represented as 

**x**ₙ = **Ax**ₙ₋₁

where **x**ₙ is the *k*-bit state vector under GF(2) of the RNG at step *n* and **A** is the *k*×*k* transition matrix who's elements are in GF(2).

```python
import numpy as np

state: int # state of the rng
k: int # amount of bits in state
A: np.ndarray # k×k transition matrix
x_n_minus_1: np.ndarray = np.array([[(state >> i) & 0b1] for i in range(k)], np.uint8) # k-bit state column vector

def next_state(x):
    return (A @ x) % 2 # Ax multiplication under GF(2)

x_n: np.ndarray = next_state(x_n_minus_1)
```

## Matrix Representation of PRNG jump

In order to jump the PRNG, one must be able to compute:

**x**ₙ₊ᵥ = **Jx**ₙ

where *v* is the amount of steps to jump and

**J** = **A**ᵛ

defines J as a matrix that describes jumping the PRNG *v* steps.

## Polynomial Representation

The characteristic polynomial of the matrix **A** can be defined as

p(z) = det(z**I** + **A**) = zᵏ + α₁zᵏ⁻¹ + ... + αₖ₋₁z + αₖ

where **I** is the identity matrix and each coefficient αⱼ is in GF(2) and thus is either 1 or 0.

The coefficients of the characteristic polynomial can be computed via sympy as shown below:

```python
import numpy as np
from sympy import Matrix
from functools import reduce
from typing import List

A: np.ndarray # k×k transition matrix

coeffs: List[int] = Matrix(A).charpoly().all_coeffs()
coeffs: int = reduce(lambda p, q: (p << 1) | (q & 1), coeffs) # q & 1 converts each coeff to GF(2)
```
The integer *coeffs* is *k*+1 bits wide and now stores each coefficient of the characteristic polynomial as individual bits.

As an example, the characteristic polynomial of [Xoroshiro128+](https://xoshiro.di.unimi.it/xoroshiro128plus.c) is as shown below:

``x**128 + x**115 + x**113 + x**111 + x**109 + x**108 + x**105 + x**104 + x**103 + x**102 + x**100 + x**98 + x**95 + x**94 + x**92 + x**91 + x**90 + x**88 + x**87 + x**86 + x**85 + x**81 + x**80 + x**79 + x**77 + x**76 + x**74 + x**72 + x**69 + x**64 + x**62 + x**60 + x**58 + x**57 + x**56 + x**55 + x**50 + x**48 + x**47 + x**45 + x**44 + x**43 + x**40 + x**36 + x**34 + x**31 + x**30 + x**29 + x**25 + x**23 + x**17 + x**13 + 1``

For this PRNG, k = 128 and the coefficients of this characterstic polynomial can be stored as the 129-bit integer ``0x10008828e513b43d5095b8f76579aa001``.

A fundamental property of the characterstic polynomial p(z) to remember is that is that:

p(**A**) = **A**ᵏ + α₁**A**ᵏ⁻¹ + ... + αₖ₋₁**A** + αₖ**I** = 0

## Jump Polynomials

If we define a polynomial g(z) as:

g(z) = zᵛ % p(z) = a₁zᵏ⁻¹ + ... + aₖ₋₁z + aₖ

and therefore:

g(z) + q(z)p(z) = zᵛ

...

g(z) = zᵛ - q(z)p(z)

for some polynomial q(z).

We can now realize that for z = **A**:

g(**A**) = **A**ᵛ - q(**A**)p(**A**)

...

g(**A**) = **A**ᵛ - q(**A**) * 0

...

g(**A**) = **A**ᵛ

...

g(**A**) = **A**ᵛ % p(**A**) = **A**ᵛ = J

...

J = **A**ᵛ = g(**A**)

## Computing Jump Polynomial

We now know that to jump ahead the PRNG we can compute **x**ₙ₊ᵥ by:

**x**ₙ₊ᵥ = **Jx**ₙ

where:

**J** = **A**ᵛ = g(**A**)

and

g(z) = zᵛ % p(z) = a₁zᵏ⁻¹ + ... + aₖ₋₁z + aₖ

g(z), or the "Jump Polynomial" can be computed via polynomial arithmetic under GF(2).

When representing GF(2) polynomials as integers who's bits are the coefficients of the polynomial, addition is effectively an XOR operation, whilst multiplication can be represented via AND operations and addition (XOR).

Exponentiation is just repeated multiplication, and for high exponents can be computed efficiently via exponentiation by squares.

Subtraction under GF(2) is identical to addition, and division (and therefore modulo) can be represented via subtraction (XOR) and bit shifts.

Computing g(z) = zᵛ % p(z) this way is done by:

```python
gf2_mod: callable # function describing the modulo operation under GF(2)
gf2_pow: callable # function describing the pow operation under GF(2)
characteristic_polynomial: int # integer that stores each coefficient of the characteristic polynomial as individual bits
jump_polynomial: int = gf2_mod(gf2_pow(2, v), characteristic_polynomial)
```

as the bits of the integer 2 (0b10) represents the polynomial z**1 or simply just z.

## Application of Jump Polynomial

The definition of **J** (the result of inputting **A** to the jump polynomial) is shown below:

**J** = **A**ᵛ = g(**A**) = a₁**A**ᵏ⁻¹ + ... + aₖ₋₁**A** + aₖ**I**

and therefore the application of this polnomial via **Jx** is defined as:

**Jx** = (a₁**A**ᵏ⁻¹ + ... + aₖ₋₁**A** + aₖ**I**)x

or

**Jx** = **A**( ... **A**(**A**(**A**a₁**x** + a₂**x**) + a₃**x**) + ... + aₖ₋₁**x**) + aₖ**x**

via Horner's method for polynomial evaluation.

Remembering that **Ax** descibes advancing the RNG 1 step, and that aⱼ is the the j-th coefficient of the jump polynomial, **Jx** can be computed via the addition of up to *k* state vectors.

This method of computing the jump can be done as follows:

```python
import numpy as np
from typing import List

state: np.ndarray # k-bit state column vector
result: np.ndarray # k-bit state column vector
A: np.ndarray # k×k transition matrix
jump_polynomial: int # integer that stores each coefficient of the jump polynomial as individual bits
k: int = state.size # amount of bits in state

for j in range(0, k):
    if (jump_polynomial >> j) & 0b1 == 1: # only add if aⱼ₊₁ == 1, otherwise Aaⱼ₊₁x = 0 and addition is pointless
        result = (result + state) % 2 # + Aaⱼ₊₁x addition under GF(2), this is equivalent to the XOR operation
    state = (A @ x) % 2 # Ax multiplication under GF(2)
    # state is now equal to Aʲ⁺¹x
```

or without matrix multiplication as:

```python
rng: object # PRNG object
rng.state: int # full state of the rng, method can easily be adapted to this being List[int]
rng.next_state: callable # method that advances the state of the rng by 1 step
result_state: int # the state of the rng after jump
jump_polynomial: int # integer that stores each coefficient of the jump polynomial as individual bits

while jump_polynomial > 0:
    if jump_polynomial & 1:
        result_state ^= rng.state
    rng.next_state()
    jump_polynomial >>= 1
rng.state = result_state
```

## Efficiently jumping an arbitrary amount of advances

Jumping *v* advances when *v* is static can easily be done by computing the jump polynomial ahead of time, but when *v* is not static it is not as simple.

### Computing jump polynomial during execution

One method of jumping an arbitrary about of advances would be to compute the jump polynomial during execution of the program and then proceeding to apply it. This method works, though it's performance greatly suffers from the expensive GF(2) modulo function that must be repeatedly run.

### Precomputed step jump polynomials

A more efficient method of jumping an arbitrary amount of advances can be done by applying multiple precomputed jump polynomials one after another.

Consider a situation where you need to jump 123 advances, if you were to advance 3 steps, then 20 steps, then 100 steps, this would be the equivalent of advancing the rng 123 steps.

This scenario represents the equality:

**A**¹²³x = **A**⁽¹⁰⁰⁺²⁰⁺³⁾x = **A**¹⁰⁰**A**²⁰**A**³x

If the goal was to be able to arbitrarily jump *v* advances where *v* is in the range 0-999 inclusive, this could be represented by jumping i steps, then j steps, and finally k steps, where:

i = v % 10

j = floor((v % 100) / 10) * 10

k = floor(v / 100) * 100

By precomputing the jump polynomial for all 10 possible values of i, all 10 possible values of j, and all 10 possible values of k, storing them in a lookup table, jumping *v* steps is easily done by applying three jump polynomials from the three tables of only 30 total values.

This idea can be more generally applied to any base-n number system with any maximum advance nˣ - 1.

The maximum amount of state advances needed to compute a jump with this method is given by:

m = k * x

and the amount of bits of memory needed to store the jump polynomials is given by:

s = k * x * (n - 1)

so it is important to find a balance between memory usage and performance for your use case.

Doing this with any base-n system where n is a power of 2 is especially simple, as the floored division is equivalent to logical right shifts and modulo is equivalent to masking bits.

Two implementations of this method (base-2 and base-256 both with maximum advance 2ᵏ - 1) are shown below:


```python
from typing import List
rng: object # PRNG object
rng.state: int # full state of the rng, method can easily be adapted to this being List[int]
rng.next_state: callable # method that advances the state of the rng by 1 step
result_state: int # the state of the rng after jump
jump_polynomials: List[int] # list of k jump polynomials that describe jumping 2**k steps
jump_count: int # amount of steps to jump
index: int = 0 # current bit position of jump_count

while jump_count > 0:
    if jump_count & 1: # equivalent of modulo 2, if there is 0 in this position we don't need to jump
        # jump 2**index steps
        jump_polynomial = jump_polynomials[index]
        while jump_polynomial > 0:
            if jump_polynomial & 1:
                result_state ^= rng.state
            rng.next_state()
            jump_polynomial >>= 1
        rng.state = result_state
    jump_count >>= 1 # equivalent of floored division by 2
    index += 1
```
```python
from typing import List
rng: object # PRNG object
rng.state: int # full state of the rng, method can easily be adapted to this being List[int]
rng.next_state: callable # method that advances the state of the rng by 1 step
result_state: int # the state of the rng after jump
jump_polynomials: List[List[int]] # list of k // 8 lists of 255 jump polynomials that describe jumping p * 2**(i * 8) steps, where i = the index of the main list and p = the index of the sub-list + 1
jump_count: int # amount of steps to jump
index: int = 0 # current byte position of jump_count

while jump_count > 0:
    position_value = jump_count & 0xFF # equivalent of modulo 256
    if position_value: # if there is 0 in this position we don't need to jump
        # jump position_value * 2**(index * 8) steps
        jump_polynomial = jump_polynomials[index][position_value - 1]
        while jump_polynomial > 0:
            if jump_polynomial & 1:
                result_state ^= rng.state
            rng.next_state()
            jump_polynomial >>= 1
        rng.state = result_state
    jump_count >>= 8 # equivalent of floored division by 256
    index += 1
```

# References
- Peter Occil - ["Notes on Jumping PRNGs Ahead"](http://peteroupc.github.io/jump.html)

- Haramoto, Matsumoto, Nishimura, Panneton, L’Ecuyer - "Efficient Jump Ahead for F2-Linear Random Number Generators"
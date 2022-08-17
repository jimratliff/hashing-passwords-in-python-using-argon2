# hashing-passwords-in-python-using-argon2
This repository demonstrates how to hash (and then verify) a password in Python using the
[Argon2 algorithm](https://github.com/P-H-C/phc-winner-argon2/blob/master/argon2-specs.pdf).

As of August 2022, when this repository was begun, Argon2 is considered the state of the art hashing algorithm. It won the 2015 [Password Hashing Competition](https://www.password-hashing.net/): “We recommend that you use Argon2 rather than legacy algorithms.”

#The format of an encoded hash
The encoded format outputs as a single string not merely the hashed password string itself but also (a) the salt and (b) information about the hashing algorithm.

In the below example, the leading section up to the third “$” describes:
* 'argon2i': That the algorithm is argon2 and which flavor (here, argon2i)
* 'v=19': Version 19 (decimal) of Argon2 (0x13 in hexadecimal)
* 'm=16': memorySizeKB: Amount of memory (in kibibytes, i.e., 1024 bytes) to use
* 't=10': iterations: Number of iterations to perform
* 'p=1': parallelism: Degree of parallelism. (Number of threads.)
```
$argon2i$v=19$m=16,t=10,p=1$dmVKdm1SMXQwd3BFa1VUOQ$T6twcxe5u7JJj2MLbvEzRg
```

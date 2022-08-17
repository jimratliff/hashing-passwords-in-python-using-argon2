"""
The below roughly follows the sample from the project description of the
argon2-cffi package on PyPI:
https://pypi.org/project/argon2-cffi/

See also Svetlin Nakov, Practical Cryptography for Developers, (in process),
in chapter Argon 2, section “Argon2 Calculation in Python — Example”
https://cryptobook.nakov.com/mac-and-key-derivation/argon2#argon2-calculation-in-python-example
"""

import argon2

incoming_password_string = input('Define the password you want to test:\n')

password_hasher = argon2.PasswordHasher()
encoded_hashed_password = password_hasher.hash(incoming_password_string)

print(f"\nHere is the resulting (encoded) hashed password string:\n{encoded_hashed_password}\n")

print("Now for the tests… (Type 'stop' to exit.)\n")
while True:
    string_to_compare = input('Enter the string to be compared against the earlier-entered password:\n')
    print(" ")

    if string_to_compare == 'stop':
        print("I have been asked to cease and desist. Of course, I obey.\n")
        break

    try:
        comparison_result = password_hasher.verify(encoded_hashed_password, string_to_compare)
    except argon2.exceptions.VerifyMismatchError:
        print("❌ NOPE! The string you typed did NOT match the stored password.")
    else:
        print("✅ CORRECT! The string you typed matched the stored password.")
    
    print("Let’s keep going. (Enter 'stop' to stop.)\n")


"""
The below roughly follows the sample from the project description of the
argon2-cffi package on PyPI:
https://pypi.org/project/argon2-cffi/

"""

# The below argon2 module is from the package argon2-cffi
#   pip install argon2-cffi
# CFFI stands for “C Foreign Function Interface.”
# argon2-cffi defends on argon2-cffi-bindings that vendors Argon2’s C code by
# default. 
# If something goes wrong, update cffi, pip, and setuptools via:
#   python -m pip install -U cffi pip setuptools
import argon2

incoming_password_string = input('\nDefine the password you want to test:\n')

password_hasher = argon2.PasswordHasher()
metadata_encoded_hashed_password = password_hasher.hash(incoming_password_string)

print(f"\nHere is the resulting (metadata-encoded) hashed password string:\n{metadata_encoded_hashed_password}\n")

print("Now for the tests… (Type 'stop' to exit.)\n")
while True:
    string_to_compare = input('Enter the string to be compared against the earlier-entered password:\n')
    print(" ")

    if string_to_compare == 'stop':
        print("I have been asked to cease and desist. Of course, I obey.\n")
        break

    try:
        # password_hasher.verify(metadata_encoded_hashed_password, string_to_compare)
        password_hasher.verify("Yippy", string_to_compare)
    except argon2.exceptions.VerifyMismatchError:
        print("❌ NOPE! The string you typed did NOT match the stored password.")
    else:
        print("✅ CORRECT! The string you typed matched the stored password.")
    
    print("\nLet’s keep going. (Enter 'stop' to stop.)\n")


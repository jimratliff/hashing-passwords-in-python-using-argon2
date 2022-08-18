# Hashing passwords (and verifying them) in Python using the Argon2 algorithm

* [The Argon2 algorithm: the best for password hashing](sdfsdfsdfsdf)
* [Using the argon2-cffi package to implement Argon2 in Python](sdfsdfsdfsdf)
    * [Installation](sfsdfsdfsdf)
    * [Using the `PasswordHasher` class to hash, verify, and update older hashes](sdfsdfsdf)
        * [The initial hashing: Converting a new user-supplied password string into an hashed string (including encoded metadata) to store in the database](sdfsfsdfsdfsdf)

## The Argon2 algorithm: the best for password hashing
This repository demonstrates how to hash (and then verify) a password in Python using the
[Argon2 algorithm](https://github.com/P-H-C/phc-winner-argon2/blob/master/argon2-specs.pdf).

As of August 2022, when this repository was begun, Argon2 is considered the state-of-the-art hashing algorithm. It won the 2015 [Password Hashing Competition](https://www.password-hashing.net/): “We recommend that you use Argon2 rather than legacy algorithms.”

More specifically, of the three variants of Argon2 (Argon2i, Argon2d, and Argon2id), Argon2id is [now considered the best variant for the use case of password hashing](https://argon2-cffi.readthedocs.io/en/latest/argon2.html#what-is-argon2). See also, from the Open Web Application Security Project (OWASP), [Password Storage Cheatsheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html#argon2id):
>There are three different versions of the algorithm, and the Argon2id variant should be used, as it provides a balanced approach to resisting both side-channel and GPU-based attacks.

Recommendations for implementers of Argon2 were codified in September 2021 in [RFC 9106](https://www.rfc-editor.org/rfc/rfc9106.html), representing the consensus of the Crypto Forum Research Group (CFRG) in the Internet Research Task Force (IRTF). The RFC characterizes Argon2id as the “primary variant” and states that:
>Argon2id __MUST__ be supported by any implementation of this document, whereas Argon2d and Argon2i __MAY__ be supported.

## Using the argon2-cffi package to implement Argon2 in Python
### Installation
This repository accesses the Argon2 algorithm via the `argon2-cffi` Python package ([PyPI](https://pypi.org/project/argon2-cffi/), [GitHub](https://github.com/hynek/argon2-cffi), [Read the Docs](https://argon2-cffi.readthedocs.io/en/latest/index.html)) to provide the Argon2 algorithm.

To install:
```
pip install argon2-cffi
```
(CFFI stands for [C Foreign Function Interface](https://cffi.readthedocs.io/en/latest/).)

If you need more-specialized information on installation, particularly if you run into any obstacles, see [§ Installation](https://argon2-cffi.readthedocs.io/en/latest/installation.html#installation) in the argon2-cffi docs.

### Using the `PasswordHasher` class to hash, verify, and update older hashes
`argon2-cffi` defines the high-level class `PasswordHasher` to (a) in the user-registration use case, hash passwords with sensible defaults and (b) in the login use case, verify them. Additionally, but much less centrally, `PasswordHasher` can  check, every time a user logs in, whether the password hash should be transparently upgraded to reflect technological changes. (This functionality is implemented as a class [in order that the hashing parameters need be verified only once](https://github.com/hynek/argon2-cffi/blob/42282cd88c74197935ec6444c6d2f9497b3b03b3/src/argon2/_password_hasher.py#L38-L40).)

[By default](https://github.com/hynek/argon2-cffi/blob/42282cd88c74197935ec6444c6d2f9497b3b03b3/src/argon2/_password_hasher.py#L34), `PasswordHasher` (a) uses the `id` variant of Argon2 and (b) uses a random salt.

To instantiate the password-hasher object:
```
import argon2
password_hasher = argon2.PasswordHasher()
```
This class has [three user-facing methods](https://github.com/hynek/argon2-cffi/blob/main/src/argon2/_password_hasher.py):
* `hash()`
* `verify()`
* `check_needs_rehash()`

#### The initial hashing: Converting a new user-supplied password string into an hashed string (including encoded metadata) to store in the database

During the registration of a new user, as well as any time a user’s password is reset, your app will receive from the user a string with the new password (denoted here `incoming_password_string`). Using the above-instantiated `password_hasher` object of the `PasswordHasher` class, this user-supplied string can be converted into a string that can be securely saved in the user database by:
```
metadata_encoded_hashed_password = password_hasher.hash(incoming_password_string)
```
By including `metadata_encoded` in the name of the variable to which the output is assigned, I mean that the output string contains not only the hashed password but also:
* information identifying the variant of Argon2 that was used and, further, the particular hashing parameters used
* the [user-specific random salt](https://auth0.com/blog/adding-salt-to-hashing-a-better-way-to-store-passwords/) that was used.

The benefit of incorporating this metadata in the returned string is that it allows the app to store just this single string in the database and this will be sufficient information for the verifier to check whether a subsequently entered string was indeed the user’s originally entered password string.

For example, suppose the user supplies the following string to define her password:
```
😉*& ☂️💩 zibet3
```
(Note that emojis and embedded spaces are fair game.)

The resulting value of `metadata_encoded_hashed_password` (i.e., of `password_hasher.hash(incoming_password_string`) is:
```
$argon2id$v=19$m=65536,t=3,p=4$Tqx/YgT/BPUc4g8QWOuSeg$cUVpgl0kUTLgHUlX5oyLZ+zsTtEHgLkYlqxBgwmyXHE
```
These strings adhere to the [PHC string format](https://github.com/P-H-C/phc-string-format/blob/master/phc-sf-spec.md).

The dollar signs (`$`) delimit the components of this metadata-encoded hashed-password string.

In the above example, the leading section up to the fourth “$” describes:
* `argon2id`: That the algorithm is argon2 and which flavor (here, `argon2id`)
* `v=19`: Version 19 (decimal) of Argon2 (0x13 in hexadecimal)
* `m=65536`: memorySizeKB: Amount of memory (in kibibytes, i.e., 1024 bytes) to use
* `t=3`: iterations: Number of iterations to perform
* `p=4`: parallelism: Degree of parallelism. (Number of threads.)

This is the information, at the later password-verification stage, that will be needed in order to hash the new string in precisely the same way that the originally supplied password string was hashed.

Between the fourth and fifth occurrences of `$` (i.e., beginning immediately after `p=4$`) is a B64 encoding of the salt. The string immediately after the last `$` is the password hash itself (encoded in B64). (See [PHC string format](https://github.com/P-H-C/phc-string-format/blob/master/phc-sf-spec.md).)

#### At login time, verify whether the newly entered password string matches the originally entered password string
Now we move to the login stage, where the user has supplied a username or email address to indicate which user she is, or purports to be, and also enters a string into the password field (denoted here by `string_to_compare`) to try to prove that she is who she claims to be.

To test that claim, we need to hash the newly entered string by precisely the same method that the password string the actual user originally supplied at registration time was hashed.

Still using the above-instantiated `password_hasher` object of the `PasswordHasher` class, we now use a different method—the `verify()` method—to (a) hash the newly supplied string and compare it to the stored password hash. We simply invoke this method:

```
password_hasher.verify(metadata_encoded_hashed_password, cleartext_string_to_compare)
```
If the user’s newly entered string is the originally created password, i.e., if hashing `cleartext_string_to_compare` matches the stored hashed password, the `verify()` method will return `True`. However, if the hashed `cleartext_string_to_compare` does not match the stored hashed password, the `verify()` method will throw a `VerifyMismatchError` exception.

So we don’t even check the return value itself. Instead we just use a `try … except` structure to look for this error. If no error occurs, the user’s newly entered string was indeed her correct password. But a `VerifyMismatchError` exception will cause her newly entered string to be rejected.

```
try:
    password_hasher.verify(metadata_encoded_hashed_password, cleartext_string_to_compare)
except argon2.exceptions.VerifyMismatchError:
    print("❌ NOPE! The string you typed did NOT match the stored password.")
else:
    print("✅ CORRECT! The string you typed matched the stored password.")
```
There are two other exceptions (`VerificationError` and `InvalidHash`) that could be raised by the `verify()` method, but neither of these should be trapped in the `try … except` block, because neither would be informative about whether the newly entered string matches the originally created password. (See the [source code](https://github.com/hynek/argon2-cffi/blob/42282cd88c74197935ec6444c6d2f9497b3b03b3/src/argon2/_password_hasher.py#L192-L197) for more details.) Either of these exceptions would prevent confirmation of a valid password. Thus, either occurring would generate a fatal error, regardless of the validity of the user’s input.

#### Progressively upgrade hash quality of previously hashed passwords
The third user-facing method of the `PasswordHasher` class is `check_needs_rehash()`. That method’s docstring explains:
> Whenever your *Argon2* parameters -- or *argon2-cffi*'s defaults! -- change, you should rehash your passwords at the next opportunity. The common approach is to do that whenever a user logs in, since that should be the only time when you have access to the cleartext password.

The `check_needs_rehash()` method checks whether the set of parameters specified in one metadata-encoded password hash is the set of parameters specified in another metadata-encoded password hash.

The procedure during a login event would be:
1. Receive a purported password string (denoted here by `incoming_password_string`) from the user that wants to log in
2. Run the `verify()` method on that string against the stored metadata-encoded password hash in the database that corresponds to this user. This means that `incoming_password_string` is the valid cleartext form of the password. 
3. If the verification is successful, run the `check_needs_rehash()` method. If that returns `True`, rehash `incoming_password_string` using the current set of parameters, and store *that* hash in the database (replace the prior version).
4. Log the user in.

For example, a login function [could look like](https://argon2-cffi.readthedocs.io/en/stable/api.html#module-argon2):
```
import argon2
password_hasher = argon2.PasswordHasher()

def login(db, user, cleartext_string_to_compare):
    currently_stored_metadata_encoded_hash_of_password = db.get_password_hash_for_user(user)

    # Verify password, raises exception if wrong.
    password_hasher.verify(currently_stored_metadata_encoded_hash_of_password, cleartext_string_to_compare)

    # Now that we have the cleartext password,
    # check the hash's parameters and if outdated,
    # rehash the user's password in the database.
    if password_hasher.check_needs_rehash(currently_stored_metadata_encoded_hash_of_password):
        db.set_password_hash_for_user(user, password_hasher.hash(cleartext_string_to_compare))
```

### Choosing parameters
See [§ Choosing parameters](https://argon2-cffi.readthedocs.io/en/stable/parameters.html#choosing-parameters) in [Read the Docs](https://argon2-cffi.readthedocs.io/en/latest/index.html).

## Transcript from running this program with example password
```
╭─(venv) ~/Documents/GitHub_repos/hashing-passwords-in-python-using-argon2  | git: main ✘ b04dcde
╰─ 🔶 python hashing_passwords_in_python_using_argon2.py

Define the password you want to test:
😉*& ☂️💩 zibet3

Here is the resulting (metadata-encoded) hashed password string:
$argon2id$v=19$m=65536,t=3,p=4$Tqx/YgT/BPUc4g8QWOuSeg$cUVpgl0kUTLgHUlX5oyLZ+zsTtEHgLkYlqxBgwmyXHE

Now for the tests… (Type 'stop' to exit.)

Enter the string to be compared against the earlier-entered password:
😉*& ☂️💩 zibet3

✅ CORRECT! The string you typed matched the stored password.

Let’s keep going. (Enter 'stop' to stop.)

Enter the string to be compared against the earlier-entered password:
😱I can’t remember the password! 😐

❌ NOPE! The string you typed did NOT match the stored password.

Let’s keep going. (Enter 'stop' to stop.)

Enter the string to be compared against the earlier-entered password:
stop

I have been asked to cease and desist. Of course, I obey.
```

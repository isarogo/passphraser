import pandas as pd
import secrets
import sys
import requests
import hashlib

df = pd.read_csv("diceware.csv", sep=",", header="infer")

# User Inputs for desired number of passwords, minimum and maximum lengths, whether first letter is capitalized, and whether you want to see the generated values and what the program's checks come up with.
try:
    num = int(sys.argv[1])
    pp_min_length = int(sys.argv[2])
    pp_max_length = int(sys.argv[3])
    title = int(sys.argv[4])
    verbose = int(sys.argv[5])
except IndexError:
    num = 1
    title = 0
    verbose = 0


# Generate the random numbers required to search the diceware list.
# These numbers are 6 digits, where each digit is within range of [1,6]


def random_num():
    secretsGenerator = secrets.SystemRandom()
    counter = 0
    number = ""
    temp = 0
    while counter < 5:
        temp = secretsGenerator.randint(1, 6)
        number += str(temp)
        counter += 1
    return int(number)

# Functions for testing security of the password


def request_api_data(query_char):
    # needs first five char of SHA1 hashed version
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(
            f'Error Fetching: {res.status_code}, check API and try again')
    return res


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)

# Main generator function. Takes the value and


def password_generator():
    passphrase = ""
    while len(passphrase) < pp_min_length:
        index = random_num()
        if verbose:
            print(index)
        if title:
            passphrase += df.loc[df['number'] == index, 'word'].iloc[0].title()
        else:
            passphrase += df.loc[df['number'] == index, 'word'].iloc[0]
    if verbose:
        print(passphrase)
    while len(passphrase) > pp_max_length:
        if verbose:
            print(
                f"Password is too long at {len(passphrase)} characters. Trying again...")
        passphrase = password_generator()
    count = pwned_api_check(passphrase)
    if count:
        if verbose:
            print("Password has been compromised. Trying Again...")
        passphrase = password_generator()
    return passphrase


for i in range(num):
    passphrase = password_generator()
    print(
        f"Your password ({i+1}/{num}) is {passphrase}. It is {len(passphrase)} characters long and not a known pwned password")

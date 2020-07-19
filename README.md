# passphraser
A python program to create an uncompromised passphrase from the diceware wordlist.

## Package Requirements
- pandas
- secrets
- sys
- requests
- hashlib

## Usage

Run
`python passphraser.py number_of_passwords min_length max_length title verbose`

Where
- *number_of_passwords* == an integer greater than 0
- *min_length* == an integer greater than 0 and less than the max_length
- *min_length* == an integer greater than the min_length
- *title* == enter `1` for capitalizing each discrete phrase or `0` for all lowercase.
- *verbose* == enter `1` to see the generated content and those that fail the tests or `0` for just the passwords.

## Example usage

`python passphraser.py 2 15 25 1 0`

results in something like:

`WieldLaityStTitan
Your password (1/2) is WieldLaityStTitan. It is 17 characters long and not a known pwned password
HarmJcSlumpAnyCon
Your password (2/2) is HarmJcSlumpAnyCon. It is 17 characters long and not a known pwned password`

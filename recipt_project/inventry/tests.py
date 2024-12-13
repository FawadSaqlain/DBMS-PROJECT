import random
import string
import string
import random

def generate_random_key(length=5):
    characters = string.ascii_lowercase + string.digits  # Only lowercase letters and digits
    random_key = ''.join(random.choices(characters, k=length))
    print( random_key )

generate_random_key()
generate_random_key()
generate_random_key()
generate_random_key()
generate_random_key()
generate_random_key()
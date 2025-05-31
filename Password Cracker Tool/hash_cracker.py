import hashlib
import itertools
import string
from concurrent.futures import ThreadPoolExecutor
import argparse

# Supported hash algorithms
hash_names = [
    'md5',
    'sha1',
    'sha224',
    'sha256',
    'sha384',
    'sha512',
]

def generate_password(min_length, max_length, characters):
    """Generate all possible passwords with given length and characters."""
    for length in range(min_length, max_length + 1):
        for pwd_tuple in itertools.product(characters, repeat=length):
            yield ''.join(pwd_tuple)

def check_hash(password, target_hash, hash_type):
    """Check if hashed password matches the target hash."""
    h = hashlib.new(hash_type)
    h.update(password.encode('utf-8'))
    return h.hexdigest() == target_hash

def crack_hash(hash_str, hash_type, min_length, max_length, characters, max_workers):
    """Attempt to crack the hash using brute force with multithreading."""
    print(f"[+] Starting crack: Hash type={hash_type}, Length={min_length}-{max_length}, Characters={characters}")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for pwd in generate_password(min_length, max_length, characters):
            futures.append(executor.submit(check_hash, pwd, hash_str, hash_type))

            # Check results as they complete
            for future in futures:
                if future.done() and future.result():
                    cracked_password = list(futures[futures.index(future)].args)[0]
                    print(f"[+] Password cracked: {cracked_password}")
                    executor.shutdown(wait=False)
                    return cracked_password

    print("[-] Password not found.")
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Password hash cracker tool")
    parser.add_argument("--hash", required=True, help="The hashed password to crack")
    parser.add_argument("--hash_type", required=True, choices=hash_names, help="Hash algorithm (md5, sha1, sha256, etc.)")
    parser.add_argument("--min_length", type=int, default=1, help="Minimum password length")
    parser.add_argument("--max_length", type=int, default=5, help="Maximum password length")
    parser.add_argument("--characters", default=string.ascii_letters + string.digits, help="Characters to use for cracking")
    parser.add_argument("--max_workers", type=int, default=4, help="Number of threads to use")

    args = parser.parse_args()

    cracked = crack_hash(
        args.hash,
        args.hash_type,
        args.min_length,
        args.max_length,
        args.characters,
        args.max_workers
    )

    if cracked:
        print(f"Password successfully cracked: {cracked}")
    else:
        print("Failed to crack the password.")

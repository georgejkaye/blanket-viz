import sys

from api.auth import get_password_hash

if __name__ == "__main__":
    hash = get_password_hash(sys.argv[1])
    print(hash)

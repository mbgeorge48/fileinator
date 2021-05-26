import os
import sys
import hashlib
import json

from config_reader import ConfigReader

HASH_STORE_DIR = os.path.normpath("hash_store")


class FileHasher:
    def __init__(self, source_path, function):
        # config = ConfigReader()
        self.file_hashes = self.scan_directories(source_path)
        self.set_function(function)

    def set_function(self, function):
        if function == "scan":
            self.write_to_file(os.path.join(HASH_STORE_DIR, "hash.json"))

    def get_file_hash(self, file):
        blocksize = 65536
        try:
            this_file = open(file, "rb")
            hasher = hashlib.md5()
            buf = this_file.read(blocksize)
            while len(buf) > 0:
                hasher.update(buf)
                buf = this_file.read(blocksize)
            this_file.close()
            return hasher.hexdigest()
        except PermissionError:
            return 1

    def scan_directories(self, root_path):
        file_hashes = {}
        counter = 0
        for root, dirs, files in os.walk(os.path.normpath(root_path)):
            print(f"Looking in {root}")
            if "$" not in os.path.split(root)[-1][0]:
                for file in files:
                    counter = counter + 1
                    file_path = os.path.join(root, file)
                    hash = self.get_file_hash(file_path)
                    if counter % 10 == 0:
                        print(
                            f"Scanned {counter} files, just scanned:\t {file} => {hash}"
                        )
                    if hash != 1:
                        file_hashes[hash] = [file, file_path]
            else:
                print("Skipping folders with a $ at the start")
        print(f"Total scanned: {counter} in {str(root_path)}")
        return file_hashes

    def write_to_file(self, path):
        if not os.path.exists(self.HASH_STORE_DIR):
            os.makedirs(self.HASH_STORE_DIR)

        file_writer = open(path, "w")
        file_writer.write(json.dumps(self.file_hashes, indent=4, sort_keys=True))
        file_writer.close()


if __name__ == "__main__":
    source_path = sys.argv[1]
    function = sys.argv[2]
    # Running manually requires a path to be passed in so that it can be scanned
    # compare isn't really something I've thought through yet
    try:
        FileHasher(source_path, function)
    except IndexError:
        print("requires a path to passed in when calling the script manually i.e.")
        print("\tpython file_hasher.py <path> <function[scan/compare]>")
    except KeyboardInterrupt:
        print("Goodbye")

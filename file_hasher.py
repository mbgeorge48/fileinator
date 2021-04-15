import os
import sys
import hashlib
import json, csv

from config_reader import ConfigReader

class FileHasher():

    HASH_STORE_DIR = os.path.normpath('hash_store')
    file_hashes = {}

    def __init__(self, root_path, function):
        config = ConfigReader()
        try:
            self.scan_directories(root_path)
        except Exception as e:
            print(e)
            sys.exit()

        if function == 'scan':
            self.write_to_file(os.path.join(self.HASH_STORE_DIR,'hash.json'))
        elif function == 'compare':
            self.compare_hashes(os.path.join(self.HASH_STORE_DIR,'hash.json'))
            self.write_to_file(os.path.join(self.HASH_STORE_DIR,'duplicates.json'))

    def scan_directories(self, root_path):
        for root, dirs, files in os.walk(os.path.normpath(root_path)):
            for file in files:
                file_path = os.path.join(root,file)
                hash = self.get_file_hash(file_path)
                if hash != 1:
                    self.file_hashes[file] = hash

    def get_file_hash(self, file):
        blocksize = 65536
        try:
            this_file = open(file, 'rb')
            hasher = hashlib.md5()
            buf = this_file.read(blocksize)
            while len(buf) > 0:
                hasher.update(buf)
                buf = this_file.read(blocksize)
            this_file.close()
            return hasher.hexdigest()
        except PermissionError:
            return 1

    def compare_hashes(self, path):
        with open(path, 'r') as hash_file:
            data=hash_file.read()
        file_data = json.loads(data)
        print(type(file_data))
        for name, hash in file_data.items():
            if hash in self.file_hashes.values():
                print(name)
                # TODO
                # Now that I can compare a path to my saved list to see if I've seen it before I need to write the duplicates to a file

    def write_to_file(self, path):
        if not os.path.exists(self.HASH_STORE_DIR):
            os.makedirs(self.HASH_STORE_DIR)

        file_writer = open(path, 'w')
        file_writer.write(json.dumps(self.file_hashes, indent=4, sort_keys=True))
        file_writer.close()

if __name__ == "__main__":
    # Running manually requires a path to be passed in so that it can be scanned
    try:
        file_hasher = FileHasher(sys.argv[1], sys.argv[2])
    except IndexError:
        print('requires a path to passed in when calling the script manually i.e.')
        print('\tpython file_hasher.py <path> <function[scan/compare]>')
    except KeyboardInterrupt:
        print('Goodbye')
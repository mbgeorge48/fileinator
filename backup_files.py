import os
import shutil
import sys
from datetime import datetime

from config_reader import ConfigReader
from file_hasher import FileHasher
from picture_backup import PictureBackupinator


class Backupinator:
    def __init__(self, source_path, destination_path, program_function, other_flags):

        self.failed_files = list()

        print("=" * 60)
        print("Welcome to the fileintor backup function")
        print(f'You have selected the "{program_function}" path')
        print("This script will look for duplicates before copying them")
        print(f"Found the following flags when called: {other_flags}")
        print("=" * 60)

        if not os.path.exists(source_path):
            print(f"The source path specified doesn't exist, please check your config")

        self.create_dir(destination_path)

        source_files = FileHasher(source_path, None).file_hashes
        destination_files = FileHasher(destination_path, None).file_hashes
        counter = 0
        for hash in source_files.keys():
            if hash not in destination_files.keys():
                counter = counter + 1
                print(
                    f"{counter}) Copying: {source_files[hash][0]} to:",
                    end=" ",
                    flush=True,
                )
                try:
                    if "pictures" not in other_flags and os.path.split:
                        self.copy_file(
                            source_path, destination_path, source_files[hash]
                        )
                    else:
                        PictureBackupinator(
                            source_path, destination_path, source_files[hash]
                        )
                except Exception as e:
                    print(f"Copy failed for {source_files[hash]}\n{e}")
                    self.failed_files.append(source_files[hash])
        print("=" * 60)
        print(f"Found a total of {counter} files to copy")
        print(f"Failed to copy {len(self.failed_files)} files")
        if len(self.failed_files) > 0:
            print("Those files are:", end=" ", flush=True)
            for file in self.failed_files:
                print(file, end=" ")
        print("=" * 60)

    def copy_file(self, source_path, destination_path, file):
        new_path = os.path.split(file[1].replace(source_path, destination_path))[0]
        self.create_dir(new_path)
        print(new_path)
        try:
            shutil.copy2(os.path.split(file[1])[0], os.path.join(new_path, file[0]))
        except Exception as e:
            print(f"Copy failed for {file}\n{e}")
            self.failed_files.append(file)

    def create_dir(self, path):
        if not os.path.exists(path):
            print(
                f"The destination path specified doesn't exist, creating it now ({path})"
            )
            os.makedirs(path, exist_ok=True)


config = ConfigReader()
local_path = os.path.normpath(config.local_path)
remote_path = os.path.normpath(config.remote_path)

if sys.argv[1] == "to-host":
    program_function = "Backup device to host"
    source_path = remote_path
    destination_path = local_path
elif sys.argv[1] == "to-remote":
    program_function = "Host to backup device"
    source_path = local_path
    destination_path = remote_path
else:
    print("Invalid function passed in when calling the script")

try:
    other_flags = []
    if sys.argv[2] == "pictures":
        other_flags.append("pictures")
except IndexError:
    pass


if __name__ == "__main__":
    time_format = "%H:%M:%S"
    start_time = datetime.now().strftime(time_format)
    print(f"Start time = {start_time}")
    try:
        Backupinator(source_path, destination_path, program_function, other_flags)
    except IndexError and NameError:
        print("requires a function to be passed in when calling the script i.e.")
        print("\tpython backup_files.py <function[to-host/to-remote]>")
    except IOError:
        print("Ran into issues reading/copying files")
        print(
            "Check you've got enough disk space/your folder permissions/your folder path"
        )
    except KeyboardInterrupt:
        print("Goodbye")
    finish_time = datetime.now().strftime(time_format)
    print(f"Finish time = {finish_time}")
    time_delta = datetime.strptime(finish_time, time_format) - datetime.strptime(
        start_time, time_format
    )
    total_seconds = time_delta.total_seconds()
    minutes = total_seconds / 60
    print(f"Time elapsed = {minutes} (minutes)")

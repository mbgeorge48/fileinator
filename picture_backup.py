import os
import shutil

RAW_FILE_TYPE = "CR3"
RAW_DIR = "raw_files"


class PictureBackupinator:
    def __init__(self, source_path, destination_path, file):
        if RAW_DIR not in destination_path:
            self.create_dir(os.path.join(destination_path, RAW_DIR))
        new_path = os.path.split(file[1].replace(source_path, destination_path))[0]
        if RAW_FILE_TYPE not in os.path.splitext(file[0])[-1]:
            self.copy_file(new_path, file)
        else:
            self.copy_file(os.path.join(new_path, RAW_DIR), file)

    def copy_file(self, new_path, file):
        self.create_dir(new_path)
        print(new_path)
        shutil.copy2(file[1], os.path.join(new_path, file[0]))

    def create_dir(self, path):
        if not os.path.exists(path):
            print(
                f"The destination path specified doesn't exist, creating it now ({path})"
            )
            os.makedirs(path, exist_ok=True)


source_path = destination_path = file = None

if __name__ == "__main__":
    # Running manually won't really work, this is desinged to be called backup_files
    try:
        PictureBackupinator(source_path, destination_path, file)
    except KeyboardInterrupt:
        print("Goodbye")

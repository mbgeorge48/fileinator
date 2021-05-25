# The Fileinator

The fileinator is a script that I'm intending to use for a whole load of file IO stuff. However, right now it can just be used two things:

* Backup files
* Generated a file with all hashes of a given directory

## Setup
Start off by installing all the required pip modules, there's nothing too out there so you may already have them all

* `pip install -r requirements.pip`

Then the two functions can be called like so:

* `python backup_files.py <function[to-host/to-remote]>`
  * The functions you can choose decide whether it's backing up file to the source system or the remote system.
  *  _Uses the paths configured in your config.yml file_

* `python file_hasher.py <path> <function[scan/compare]>`
  * First off the compare funtion doesn't do anything yet and may just get removed down the line
  * If you choose to scan then it will scan every file in the path you give it and then save all the file names and their hash value (MD5) into hash_store/hash.json
  * This function was mainly made to be used with the backup_files function (So it will avoid duplicating files)


### Config
Right now there are 4 config options

* windows_hostname
* mac_hostname
* local_path
* remote_path

Both the windows and the mac hostname ones aren't used...

_They are left over from an older version of the script that I've now migrated into the Fileinator_

The important ones are the local and remote paths as they are how the backup_files function finds all your files. The script should accept both windows and unix paths however at the time of writing this I've haven't tested it on windows!
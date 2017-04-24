# yasp
Yet Another Syncing Program (based on rsync)
## Installation
1. Add `yasp.py` to you bin
  * Copy it to `~/bin` (assuming `~/bin` is in your path)
  * Copy it to `/bin` (requires root)
2. Create the file `.yasprc` in your home directory. It should look something like this:
``` ini
[main]
source_path = /home/user/tv_shows
destination_path = /home/user/video_files
rsync_options = --progress --recursive
file_list = /home/user/.yasp_files # this is the list of files which will be synced

[remote]
remote = source # 'source' or 'destination'
protocol = ssh # 'ssh' or 'rsync-daemon'
user = user # username 
ip = 8.8.8.8 # address of remote pc
key = # optional auth key 

[loop] 
interval = 60
last_digest = this_can_be_anything_but_do_not_edit_it_afterwards
```
## Dependencies
The two programs this uses are installed on most linux boxes by default
* `rsync`
* `find`

## Usage
1. (optional) run `$ yasp.py -c` to create initial file list using find at specified location (in `.yasprc`)
2. `$ yasp.py` or `$ yasp.py &` to run it as a background process
3. Mark desired files in file list with `x` before the file path (make sure to include a space)

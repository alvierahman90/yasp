#!/usr/bin/env python3

import argparse
import configparser
import os


#DONE
def load_config( config_filename ):
	config = configparser.ConfigParser()
	config.read(config_filename)
	return config


#TODO validate config
def validate_config( config ):
	pass


#DONE
def write_config( config, config_filename ):
	with open(config_filename,"w") as file:
		config.write(file)


#DONE
def create_file_list( args, config ):
	# generate file list
	if config['remote']['remote'] == "disabled" or config['remote']['remote'] == "destination" :
		os.system("cd /;  find " + config['main']['source_path']
				+ " > "
				+ config['main']['source_path'] + "/.rsync_selection_list")
		os.system("cp "
				+ config['main']['source_path'] + "/.rsync_selection_list"
				+ " ./" + config['main']['file_list'])
	elif config['remote']['remote'] == "source" :
		os.system("ssh "
				+ config['remote']['user'] + "@" + config['remote']['ip']
				+ " find " + config['main']['source_path']
				+ " \> "
				+ config['main']['source_path'] + "/.rsync_selection_list")
		os.system("scp "
				+ config['remote']['user'] + "@" + config['remote']['ip']
				+ ":" + config['main']['source_path'] + "/.rsync_selection_list"
				+ " ./" + config['main']['file_list'])

	# print a list of files
	# if args.verbose >= 3 :
		# with open(config['main']['file_list'], "r") as file :
		#	files_in_source = file.read()
		# print("Files in source:")
		# for i in range(len(files_in_source)) :
		#	print(files_in_source[i])


#TODO merge lists
def merge_list( args, list_1, list_2):
	pass # application does not delete files yet. Do not need to merge


#DONE create sync list
def create_to_sync_list( args, config ):
	with open(config['main']['file_list']) as file:
		file_list = file.read()
	file_list = file_list.split("\n")
	sync_list = []
	for i in range(len(file_list)):
		try:
			if file_list[i].split("x ")[0] == "":
				print("Files in sync list:")
				print(file_list[i])
				sync_list.append(file_list[i].split("x ")[1])
		except:
			pass
	return sync_list


#DONE actual syncing
def sync( args, config_file, sync_list ):
	if config_file['remote']['remote'] == "disabled" :
		for i in range(len(sync_list)) :
			if args.verbose >= 1 :
				print("rsync command:\n" + "rsync " + sync_list[i] + " " + config_file['main']['destination_path'])
			os.system("rsync " + sync_list[i] + " " + config_file['main']['destination_path'])
		# if one of the paths is remote
	else :
		# sets appropriate colon for rsync or ssh
		if config_file['remote']['protocol'] == "ssh" :
			colon = ":"
		elif config_file['remote']['protocol'] == "rsync-daemon" :
			colon = "::"
		# execute appropriate rsync commands
		if config_file['remote']['remote'] == "source" :
			for i in range(len(sync_list)) :
				if args.verbose >= 1 :
					print("rsync command: rsync "
					      + config_file['main']['rsync_options']
					      + " "
					      + config_file['remote']['user']
					      + "@"
					      + config_file['remote']['ip']
					      + colon + "\""
					      + sync_list[i]
					      + "\" "
					      + config_file['main']['destination_path'])
				os.system("rsync "
				          + config_file['main']['rsync_options']
				          + " "
				          + config_file['remote']['user']
				          + "@"
				          + config_file['remote']['ip']
				          + colon + "\""
				          + sync_list[i]
				          + "\" "
				          + config_file['main']['destination_path'])
		#TODO sort out destination syncing
		elif config_file['remote']['remote'] == "destination" :
			for i in range(len(sync_list)) :
				if args.verbose >= 1 :
					print("rsync "
					      + config_file['main']['rsync_options']
					      + " "
					      + sync_list[i]
					      + " "
					      + config_file['remote']['user']
					      + "@"
					      + config_file['remote']['ip']
					      + ":"
					      + config_file['main']['destination_path'])
				os.system("rsync "
				          + config_file['main']['rsync_options']
				          + " "
				          + sync_list[i]
				          + " "
				          + config_file['remote']['user']
				          + "@"
				          + config_file['remote']['ip']
				          + ":"
				          + config_file['main']['destination_path'])


#TODO listen loop
def loop( args, config):
	from hashlib import sha256
	from time import gmtime, sleep, strftime
	while True:
		last_digest = config['loop']['last_digest']
		with open(config['main']['file_list'], "rb") as file:
			to_sync_binary = file.read()
		sha = sha256()
		sha.update(to_sync_binary)
		digest = sha.hexdigest()
		print("Digest as of " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) +": "+ digest)
		if digest != last_digest:
			sync( args, config, create_to_sync_list(args, config))
			config['loop']['last_digest'] = digest
			with open("remote_iync.ini","w") as file:
				config.write(file)
		sleep(float(config['loop']['interval']))

def main():
	config = load_config( "remote_iync.ini" )

	validate_config(config)

	parser = argparse.ArgumentParser(prog="rsync-selection"
		, description="Selectively sync parts of a directory")

	parser.add_argument("-v", "--verbose"
		, action="count"
		, default=0
		, help="Increases verbosity")

	parser.add_argument("-c", "--create-file-list"
		, action="store_true"
		, default=False
		, help="Generates list of files then exits")

	parser.add_argument("-m", "--merge"
		, action="store_true"
		, default=False
		, help="TODO - Retrieves up to date version of file list and merges with current to sync list then quits")

	parser.add_argument("-l", "--loop"
		, action="store_true"
		, default=False
		, help="Run as constant loop")

	parser.add_argument("-i", "--loop-interval"
		, type=int
		, default=config['loop']['interval']
		, help="Change the interval between loops in seconds.\nDefaults to what is stated in config file.")

	args = parser.parse_args()

	if not args.loop:
		print("Not set to listen... ")
		sync( args, config, create_to_sync_list(args, config))
	else:
		loop(args, config)


if __name__ == '__main__' :
	main()


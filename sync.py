import subprocess
import os
import sys

# try to load an adb shell, print errors to the console if it goes wrong
# there are a lot of ways trying to open an adb shell can go wrong, so the user can handle them if they do
def load_adb():
	adb = subprocess.Popen(["adb", "shell"], stderr=subprocess.PIPE,stdin=subprocess.PIPE, text=True, encoding="utf-8")
	print("adb starting...")
	try:
		adb.wait(1)
	except subprocess.TimeoutExpired:
		print("adb shell successfully connected!")
		return adb
	else:
		adb_output = adb.stderr.readline()
		if len(adb_output):
			print(adb_output)
		return None

# basic wrapper to run a command via our adb shell and log it to the console
def run_adb(command):
	print(command)
	adb.stdin.write(command)

# I'm not including an entire yaml library here, custom config loader go!
# returns a dict by default, a list of k/v pairs if `load_as_pairs` is set (use when keys may not be unique)
def load_kv_file(path, delimiter = "=", comment = "#", load_as_pairs = False):
	if load_as_pairs:
		values = []
	else:
		values = {}

	try:
		with open(path, "r") as file:
			file_lines = file.read().splitlines()
	except:
		return values
	
	for line in file_lines:
		if line.startswith(comment):
			continue
		split = line.split(delimiter, 1)
		if len(split) < 2:
			continue
		prop, value = split
		if load_as_pairs:
			values.append((prop, value))
		else:
			values[prop] = value
	return values

# Delete any local files that have been removed from the playlist
def cleanup_removed(archive, do_removal = True):
	print("Checking for removed tracks...")
	downloaded_files = os.listdir(config["storage_path"])
	if not len(downloaded_files):
		print("No downloaded tracks found, skipping removed track checks.")
		return

	id_check_process = subprocess.Popen(f"yt-dlp --flat-playlist --print id {config['playlist_url']}", stdout=subprocess.PIPE, text=True)
	while True:
		try:
			id_check_process.wait(1)
		except subprocess.TimeoutExpired:
			pass
		else:
			playlist_ids = id_check_process.stdout.read().splitlines()
			break

	# print(f"playlist_ids: {playlist_ids}")
	for pair in archive:
		archive_id = pair[1]
		if archive_id in playlist_ids:
			# it's still in the playlist, we're fine
			continue
		print(f"Found removed track with ID {archive_id}")
		if not do_removal:
			continue
		# not in the playlist, delete
		filename = find_file(downloaded_files, archive_id)
		if not filename:
			print(f"Removed track present in archive but not on disk, cleaning up...")
			continue

		
		print("Deleting removed track from phone via adb...")
		run_adb(f"rm \"{config['phone_path']}/{filename}\"")

		print("Deleting removed track from disk...")
		os.remove(f"{config['storage_path']}/{filename}")

		archive.remove(pair)

	#write the ones still in our archive back to the file
	print(f"Writing back to archive...")
	with open("archive.txt", "w") as archive_file:
		for pair in archive:
			archive_file.write(f"{pair[0]} {pair[1]}\n")
		
def find_file(files_list, id):
	for filepath in files_list:
		if id in filepath:
			return filepath
	return None


adb = load_adb()
if not adb:
	quit()

config_path = "config.txt"
# gitignored local config for source control purposes
if os.path.isfile("_config.txt"):
	config_path = "_config.txt"

config = load_kv_file(config_path, "=", "--")
if config == {}:
	raise FileNotFoundError('Unable to load values from config.txt')

if not os.path.isdir(config["storage_path"]):
	print(f"Creating new folder for storage at {config['storage_path']}")
	os.makedirs(config["storage_path"])

archive = load_kv_file("archive.txt", " ", load_as_pairs=True)
if archive != []:
	cleanup_removed(archive, not ("--warn" in sys.argv))
else:
	print("No archive found, skipping removed tracks check.")

print()
print("Starting main sync download...")
download = subprocess.run(f"yt-dlp.exe -x --audio-format {config['format']} --download-archive archive.txt {config['playlist_url']} -P {config['storage_path']}")
print()

print("Starting adb push copy...")
subprocess.run(f"adb push --sync ./Downloaded/. {config['phone_path']}")
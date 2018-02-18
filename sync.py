import argparse
import youtube_dl
import os
import shutil

# arguments #
playlist_url = None
sync_folder = None

parser = argparse.ArgumentParser(description='YT playlist downloader')
parser.add_argument('-p', metavar='playlist', type=str, nargs=1, help='URL of YT playlist', required=True,dest='playlist_url')
parser.add_argument('-l', metavar='sync folder', type=str, nargs=1, help='Folder to push downloaded files to for syncing (e.g. Dropbox)', dest='sync_folder')
args = parser.parse_args()

playlist_url = args.playlist_url[0]
sync_folder = args.sync_folder[0]

dir_path = os.path.dirname(os.path.realpath(__file__))

# download files #
def download_files(URL):
	options = {
		'format':'bestaudio/best',
		'extractaudio':True,
		'audioformat':'mp3',
		'outtmpl':os.path.join(dir_path,'./Output/') + u'%(id)s.%(ext)s',
		'download_archive':os.path.join(dir_path,'./youtube_archive'),
		'ignoreerrors':True,
		'nooverwrites':True,
		'writethumbnail':True,
		'nocheckcertificate':True,
		'postprocessors':[{
			'key':'FFmpegExtractAudio',
			'preferredcodec':'mp3',
			'preferredquality':'192',
		},
		{'key':'EmbedThumbnail'},
		{'key':'FFmpegMetadata'},
		]
	}

	with youtube_dl.YoutubeDL(options) as ydl:
		ydl.download([URL])

# move files to sync directory #
def push_files(dest_folder):
	if (dest_folder == None):
		return
	
	# file move archive #
	sync_archive = []
	if not os.path.isfile(os.path.join(dir_path,'./sync_archive')):
		f = open(os.path.join(dir_path,'./sync_archive'),'w')
		f.close()
	
	with open(os.path.join(dir_path,'./sync_archive'),'r') as f:
		sync_archive = f.readlines()
	sync_archive = [x.strip() for x in sync_archive]
	
	# find and copy the files #
	files = [f for f in os.listdir(os.path.join(dir_path,'./Output')) if os.path.isfile(os.path.join(os.path.join(dir_path,'./Output'),f))]
	for file in files:
		if (file == 'desktop.ini'):
			continue
		
		if (file in sync_archive):
			print('Skipping file ' + file + ' because it has already been copied before')
			continue
		
		if (os.path.isfile(os.path.join(dest_folder,file))):
			print('Skipping file ' + file + ' because it is already in the sync folder')
			continue
		
		print('Copying file ' + file + ' to sync folder')
		shutil.copy2(os.path.join(dir_path,'./Output/') + file,dest_folder)
		with open(os.path.join(dir_path,'./sync_archive'),'a') as f:
			f.write(file + '\n')

download_files(playlist_url)
push_files(sync_folder)
print('Done')
#This script takes a user input for an image and extract meta data and output the meta data to a .txt file
#This script also checks the MD5 hash for an image and compare it in the provided hash list.
#If hash is found in the database, Output a warning to the screen and warn the user this is a illicit image.
#!/usr/bin/python3

import argparse
import hashlib
from PIL import Image
from PIL.ExifTags import TAGS

def getMetaData(imgname, out):
	try:
		metaData = {}

		imgFile = Image.open(imgname)
		print ("Getting meta data...")
		info = imgFile._getexif()
		if info:
			print ("Found meta data!")
			for (tag, value) in info.items():
				tagname = TAGS.get(tag, tag)
				metaData[tagname] = value
				if not out:
					print (tagname, value)

			if out:
				print ("Outputting to file...  metaData of this image is stored in "+out)
				with open(out, 'w') as f:
					for (tagname, value) in metaData.items():
						f.write(str(tagname)+"\t"+\
							str(value)+"\n")
		else:
			print ("No metaData Found!")
		
	except:
		print ("Failed")

def checkHashes(imgname):
	hasher = hashlib.md5()
	with open(imgname, 'rb') as afile:
		buf = afile.read()
		hasher.update(buf)
	print('The MD5 Hash of '+imgname+' is: '+hasher.hexdigest())
	imgHashes=hasher.hexdigest()
	if imgHashes in open('hash_list.txt').read():
		print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!WARNING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		print ("!!!!!!!!!!!!Image hash found in FBI Image Hash Database!!!!!!!!!!!!")
		print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
	else:
		print ("The image is safe to view, image hash is not found in FBI Image Hash Database.")


def Main():
	parser = argparse.ArgumentParser()
	parser.add_argument("img", help="Name of an image File")
	parser.add_argument("--output","-o", help="Dump data out to File.")
	args = parser.parse_args()
	if args.img:
		getMetaData(args.img, args.output)
		checkHashes(args.img)
	else:
		print (parser.usage)

if __name__ == '__main__':
	Main()
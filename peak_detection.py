import sigmf
import zipfile
import py7zr

import os
import numpy as np
import top_block
import time
import sys
from datetime import datetime

def createMetadata(namePath, sampleRate, centerFreq):
	meta = sigmf.SigMFFile(
		data_file = namePath + ".sigmf-data",
		global_info = {
			sigmf.SigMFFile.DATATYPE_KEY: "cf32",
			sigmf.SigMFFile.SAMPLE_RATE_KEY: sampleRate,
			sigmf.SigMFFile.AUTHOR_KEY: "IMT",
			sigmf.SigMFFile.DESCRIPTION_KEY: "Placeholder",
			sigmf.SigMFFile.VERSION_KEY: sigmf.__version__,
		}
	)

	meta.add_capture(0, 
		metadata = {
			sigmf.SigMFFile.FREQUENCY_KEY: centerFreq,
			sigmf.SigMFFile.DATETIME_KEY: datetime.utcnow().isoformat()+'Z',
		}
	)

	assert meta.validate()
	metaPath = namePath + ".sigmf-meta"
	meta.tofile(metaPath)

	return (metaPath)

def fileCompress(inputFiles, outputZipName):
	"""
	zipType = zipfile.ZIP_DEFLATED
	print(f" *** Input File: {inputFiles}")
	print(f" *** Output File: {outputZipName}")

	zf = zipfile.ZipFile(outputZipName, mode="w", compression = zipType)

	try:
		for file in inputFiles:
			print(f" *** Processing File: {file}")
			zf.write(file, file.split("/")[-1])
	except FileNotFoundError as e:
		print(f" *** Exception during compression: {e}")
	finally:
		zf.close()
	"""

	print(f" *** Input File: {inputFiles}")
	print(f" *** Output File: {outputZipName}")
	try:
		with py7zr.SevenZipFile(outputZipName, "w") as archive:
			for file in inputFiles:
				print(f" *** Processing File: {file}")
				archive.write(file, file.split("/")[-1])
	except FileNotFoundError as e:
		print(f" *** Exception during compression: {e}")

def main():
	while(1):
		print("Start")
		exitCode = os.system("python3 ./top_block.py")
		File = open("ooga_booga.txt", "r")
		freq = File.readline().strip()
		time = File.readline().strip()
		samp_rate = File.readline().strip()
		data_path = File.readline().strip()
		name_path = data_path.rsplit(".", 1)[0]

		print(f"\ndata_path is {data_path}\n")
		print(f"\nname_path is {name_path}\n")

		if(exitCode != 0):
			try:
				#t1 = threading.Thread(target = signal_recorder.mainBoy, args = (freq,) )
				print("python3 ./signal_recorder.py --center-freq "+ freq + " --time " + time + " --samp-rate " + samp_rate + " --path-name " + data_path)
				os.system("python3 ./signal_recorder.py --center-freq "+ freq + " --time " + time + " --samp-rate " + samp_rate + " --path-name " + data_path)
			except:
				print("Unexpected error:", sys.exc_info()[0])
			finally:
				print("hold this place for me")
				meta_path = createMetadata(name_path, int(samp_rate), float(freq))
				files = [data_path, meta_path]
				print(files)
				fileCompress(files, (name_path + ".7z"))
		else:
			break
		print("Stop")
		

if __name__ == "__main__":
	main()
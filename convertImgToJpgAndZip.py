# pip3 install ffmpeg-python
import ffmpeg

import os
import time, shutil
from multiprocessing import Pool, cpu_count

inputDir = 'input'
outputDir = 'output'

fileObj = open('./run.log', 'a+', encoding='utf-8')
def printLog(msg):
	try:
		if type(msg) != str:
			msg = str(msg)
		msg = time.strftime('%Y-%m-%d %H:%M:%S') + ': ' + msg
		print(msg)
		fileObj.write(msg + '\n')
		fileObj.flush()
	except Exception as e:
		print(e)

def convertFile(fullFile, fnameNoExt, fullOutputDir):
	# print(fullFile, fnameNoExt, fullOutputDir)

	# ffmpeg convert
	stream = ffmpeg.input(fullFile)
	stream = ffmpeg.output(stream, fullOutputDir + '/' + fnameNoExt + '.jpg', loglevel='quiet')
	stream = ffmpeg.overwrite_output(stream)
	ffmpeg.run(stream)

	# # just copy file
	# shutil.copy(fullFile, fullOutputDir)

def convertDir(fullInputDir, fullOutputDir):
	if os.path.exists(fullOutputDir) == False:
		os.mkdir(fullOutputDir)

	for fname in os.listdir(fullInputDir):
		if os.path.isdir(fullInputDir + '/' + fname):
			convertDir(fullInputDir + '/' + fname, fullOutputDir + '/' + fname)
			continue
		fnameNoExt = os.path.splitext(fname)[0]
		ext = os.path.splitext(fname)[-1].upper()
		if ext != '.JPG' and ext != '.JPEG' and ext != '.PNG':
			continue

		fullFile = fullInputDir + '/' + fname
		convertFile(fullFile, fnameNoExt, fullOutputDir)

def zipDir(fullOutputDir):
	shutil.make_archive(fullOutputDir, 'zip', fullOutputDir)

def clearDir(fullInputDir, fullOutputDir):
	shutil.rmtree(fullInputDir)
	shutil.rmtree(fullOutputDir)

def processDir(dirName):
	fullInputDir = inputDir + '/' + dirName
	fullOutputDir = outputDir + '/' + dirName
	
	if os.path.isdir(fullInputDir) == False:
		return

	printLog('processing' + dirName)

	printLog('convert: ' + dirName)
	convertDir(fullInputDir, fullOutputDir)
	printLog('convert DONE: ' + dirName)

	printLog('zip: ' + dirName)
	zipDir(fullOutputDir)
	printLog('zip DONE: ' + dirName)

	printLog('clearDir: ' + dirName)
	clearDir(fullInputDir, fullOutputDir)
	printLog('clearDir DONE: ' + dirName)

	printLog('processing SUCESS' + dirName)
	printLog('')

def main():
	cpus = cpu_count()
	if cpus > 1:
		cpus = cpus - 1
	
	p = Pool(cpus)
	for dirName in os.listdir(inputDir):
		res = p.apply_async(processDir, (dirName, ))

	p.close()
	p.join()

if __name__ == '__main__':
	main()
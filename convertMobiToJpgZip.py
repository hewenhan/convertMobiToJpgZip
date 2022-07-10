# pip3 install mobi
# pip3 install ffmpeg-python
import ffmpeg
import os
import json, asyncio, time, datetime, sys, atexit, serial, shutil
from multiprocessing import Pool, cpu_count

inputDir = 'input'
outputDir = 'output'
# outputDir = 'H:/Comic'

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

def clearInputFile(fullInputDir):
	shutil.rmtree(fullInputDir)

def zipDir(fullInputDir, fnameNoExt, fullOutputDir):
	shutil.make_archive(fullOutputDir, 'zip', fullInputDir + '/' + fnameNoExt)

def convertFile(fullFile, fnameNoExt, fullOutputDir):
	stream = ffmpeg.input(fullFile)
	stream = ffmpeg.output(stream, fullOutputDir + '/' + fnameNoExt + '.jpg')
	stream = ffmpeg.overwrite_output(stream)
	ffmpeg.run(stream)

def convertDir(fullInputDir, fnameNoExt):
	fullOutputDir = fullInputDir + '/' + fnameNoExt
	fullInputDir = fullInputDir + '/mobi8/OEBPS/Images'
	if os.path.exists(fullOutputDir) == False:
		os.mkdir(fullOutputDir)

	for fname in os.listdir(fullInputDir):
		fnameNoExt = os.path.splitext(fname)[0]

		fullFile = fullInputDir + '/' + fname
		convertFile(fullFile, fnameNoExt, fullOutputDir)

def extractFile(fileFullName):
	flag = os.system('mobiunpack -i ' + fileFullName)
	if flag != 0:
		return False
	return True

def processMobi(fname):
	ext = os.path.splitext(fname)[-1].upper()
	fnameNoExt = os.path.splitext(fname)[0]

	fileFullName = inputDir + '/' + fname
	fullInputDir = inputDir + '/' + fnameNoExt
	fullOutputDir = outputDir + '/' + fnameNoExt

	if ext in [".MOBI", ".PRC", ".AZW", ".AZW3", ".AZW4"]:
		printLog('processing file: ' + fname)

		printLog('extracting: ' + fnameNoExt)
		r = extractFile(fileFullName)
		if r == False:
			printLog('extracting ERROR: ' + fnameNoExt)
			return
		printLog('extracting done: ' + fnameNoExt)

		printLog('removeing file: ' + fileFullName)
		os.remove(fileFullName)
		printLog('removeing done: ' + fileFullName)

		printLog('converting images: ' + fnameNoExt)
		convertDir(fullInputDir, fnameNoExt)
		printLog('converting done: ' + fnameNoExt)

		printLog('zip: ' + fnameNoExt)
		zipDir(fullInputDir, fnameNoExt, fullOutputDir)
		printLog('zip DONE: ' + fnameNoExt)

		printLog('clearing: ' + fnameNoExt)
		shutil.rmtree(fullInputDir)
		printLog('clearing done: ' + fnameNoExt)

		printLog('processing SUCCESS: ' + fname)

def main():

	cpus = cpu_count()
	if cpus > 1:
		cpus = cpus - 1

	p = Pool(cpus)
	for fname in os.listdir(inputDir):
		res = p.apply_async(processMobi, (fname, ))

	p.close()
	p.join()

if __name__ == '__main__':
	main()
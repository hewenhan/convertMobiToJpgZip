# pip3 install mobi
import os
import json, asyncio, time, datetime, sys, atexit, serial, shutil
from multiprocessing import Pool

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

def moveImgDirToOutput(fnameNoExt):
	srcDir = inputDir + '/' + fnameNoExt
	dstDir = outputDir + '/' + fnameNoExt

	shutil.move(srcDir + '/mobi8/OEBPS/Images', outputDir)
	os.rename(outputDir + '/Images', dstDir)
	shutil.rmtree(srcDir)

def extractFile(fileFullName):
	flag = os.system('mobiunpack -i ' + fileFullName)
	if flag != 0:
		printLog('extractFile ERROR: ' + fileFullName)
		return

def processMobi(fname):
	ext = os.path.splitext(fname)[-1].upper()
	fnameNoExt = os.path.splitext(fname)[0]
	if ext in [".MOBI", ".PRC", ".AZW", ".AZW3", ".AZW4"]:
		fileFullName = inputDir + '/' + fname
		printLog('processing file: ' + fname)

		printLog('extracting')
		extractFile(fileFullName)
		printLog('extracting done')

		printLog('clearing')
		moveImgDirToOutput(fnameNoExt)
		printLog('clearing done')

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
#!/usr/bin/env python3

# pip3 install mobi ffmpeg-python py7zr
import ffmpeg, os, time, shutil, mobi, py7zr
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

def clearInputFile(fullInputDir):
	shutil.rmtree(fullInputDir)

def archiveDir(fullInputDir, fnameNoExt, fullOutputDir):
	with py7zr.SevenZipFile(f"{fullOutputDir}.7z", 'w') as archive:
		fileFullDir = fullInputDir + '/' + fnameNoExt
		printLog(f'archiving: {fileFullDir} to {fullOutputDir}.7z')
		archive.writeall(fullInputDir + '/' + fnameNoExt, '/')

def convertFile(fullFile, fnameNoExt, fullOutputDir):
	stream = ffmpeg.input(fullFile)
	stream = ffmpeg.output(stream, fullOutputDir + '/' + fnameNoExt + '.jpg', loglevel='quiet')
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
	tempdir, filepath = mobi.extract(fileFullName)
	return tempdir, filepath

def processMobi(fname):
	ext = os.path.splitext(fname)[-1].upper()
	fnameNoExt = os.path.splitext(fname)[0]

	fileFullName = inputDir + '/' + fname
	fullInputDir = inputDir + '/' + fnameNoExt
	fullOutputDir = outputDir + '/' + fnameNoExt

	if ext in [".MOBI", ".PRC", ".AZW", ".AZW3", ".AZW4"]:
		printLog('processing file: ' + fname)

		printLog('extracting: ' + fnameNoExt)
		tempdir, filepath = extractFile(fileFullName)
		printLog('extracting done: ' + fnameNoExt)

		printLog(tempdir)
		printLog(filepath)

		printLog('removeing file: ' + fileFullName)
		os.remove(fileFullName)
		printLog('removeing done: ' + fileFullName)

		printLog('converting images: ' + fnameNoExt)
		convertDir(tempdir, fnameNoExt)
		printLog('converting done: ' + fnameNoExt)

		printLog('zip: ' + fnameNoExt)
		archiveDir(tempdir, fnameNoExt, fullOutputDir)
		printLog('zip DONE: ' + fnameNoExt)

		printLog('clearing: ' + fnameNoExt)
		shutil.rmtree(tempdir)
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
# 这是个用于将zip文件名转换为utf-8编码的脚本，用于解决windows下zip文件名乱码的问题。

# pip3 install mobi ffmpeg-python py7zr
import ffmpeg, os, time, shutil, mobi, py7zr, zipfile
from multiprocessing import Pool, cpu_count

inputDir = 'input'
outputDir = 'output'

thisDir = os.path.dirname(os.path.realpath(__file__))
inputDir = os.path.join(thisDir, inputDir)
outputDir = os.path.join(thisDir, outputDir)

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
		
def clearInputFile():
	shutil.rmtree(inputDir)

def processZipFile(fullFile, fnameNoExt):
	with zipfile.ZipFile(fullFile, 'r') as archive:
		fileList = archive.namelist()
		if len(fileList) != 1 or fileList[0].endswith('/'):
			# only 1 file, extract to outputDir
			printLog(f'{fnameNoExt} has more than 1 file')
			return
		
		extractName = fileList[0]
		archive.extractall(outputDir)
		archive.close()

	# rename the extracted file
	extractedFile = os.path.join(outputDir, extractName)
	extractNameExt = os.path.splitext(extractName)[-1]
	newExtractedFile = os.path.join(outputDir, f'{fnameNoExt}{extractNameExt}')

	printLog(f'renaming {extractedFile} to {newExtractedFile}')
	os.rename(extractedFile, newExtractedFile)

	# archive the extracted file
	zipOutputFile = os.path.join(outputDir, fnameNoExt)
	with py7zr.SevenZipFile(f"{zipOutputFile}.7z", 'w') as archive:
		printLog(f'archiving: {newExtractedFile} to {zipOutputFile}.7z')
		archive.write(newExtractedFile, os.path.basename(newExtractedFile))

	# remove the extracted file
	os.remove(newExtractedFile)

	# remove the original zip file
	os.remove(fullFile)

def processFile(fname):
	printLog('processing file: ' + fname)
	ext = os.path.splitext(fname)[-1].upper()
	fnameNoExt = os.path.splitext(fname)[0]
	fullFile = os.path.join(inputDir, fname)
	if ext in [".ZIP"]:
		printLog(f'fullFile: {fullFile}')
		processZipFile(fullFile, fnameNoExt)

def main():
	printLog('Start')

	cpus = cpu_count()
	if cpus > 1:
		cpus = cpus - 1

	p = Pool(cpus)
	for fname in os.listdir(inputDir):
		res = p.apply_async(processFile, (fname, ))

	p.close()
	p.join()

if __name__ == '__main__':
	main()
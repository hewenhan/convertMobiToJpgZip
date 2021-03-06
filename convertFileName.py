# coding: utf-8

import os, glob, chardet

# convert file name remove "[Comic]" and "[Mox.moe]" and replace "[]" with "_" from input folder
def main():
	inputDir = 'input'
	outputDir = 'output'

	for root, dirs, files in os.walk(inputDir):
		for file in files:
			fullFilename = os.path.join(root, file)
			convertedFilename = file.replace('[Comic]', '').replace('[Mox.moe]', '').replace('[', '').replace(']', '_').replace(' ', '_').replace('(', '_').replace(')', '_')
			convertedFullFilename = os.path.join(root, convertedFilename)
			os.rename(fullFilename, convertedFullFilename)
			print(convertedFullFilename)

if __name__ == '__main__':
	main()

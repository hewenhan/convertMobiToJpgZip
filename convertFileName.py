# coding: utf-8
#!/usr/bin/env python3

import os

# convert file name remove "[Comic]" and "[Mox.moe]" and replace "[]" with "_" from input folder
def main():
	inputDir = 'input'

	for root, dirs, files in os.walk(inputDir):
		for file in files:
			fullFilename = os.path.join(root, file)
			convertedFilename = file.replace('[Kmoe]', '').replace('[Comic]', '').replace('[Vol.moe]', '').replace('[Mox.moe]', '').replace('[', '').replace(']', '_').replace(' ', '_').replace('(', '_').replace(')', '_')
			convertedFullFilename = os.path.join(root, convertedFilename)
			os.rename(fullFilename, convertedFullFilename)
			print(convertedFullFilename)

if __name__ == '__main__':
	main()

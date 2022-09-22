
Convert Mobi To Image
====

author:  `Blind Holmes`
version: `1.2.0`
> Written with [https://stackedit.hewenhan.me/](https://stackedit.hewenhan.me/).

## Introduction

Use multiple processes to convert Mobi to image folders, or convert to JPG compressed zip packages.

## Installation

```
pip3 install mobi
pip3 install ffmpeg-python
git clone https://github.com/hewenhan/convertMobiToImage.git
```

## Usage

Put the `.mobi` file in the input folder. Execute `convertMobiToJpgZip.py`. After the conversion is complete, The filename is input .mobi name contain converted `.jpg` file's zip file is generated in the output folder.

```
python3 convertMobiToImage.py
```

Put the `.mobi` file in the input folder. Execute `convertMobiToImage.py`. After the conversion is complete, a folder of images sets is named with the filename of each mobi file and generated in the output folder.

```
python3 convertMobiToImage.py
```

Put the `images folder` in the input folder. Execute `convertImgToJpgAndZip.py`. After the conversion is complete, The filename is input folder name contain converted `.jpg` file's zip file is generated in the output folder.
```
python3 convertImgToJpgAndZip.py
```
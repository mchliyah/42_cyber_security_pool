
# Project: Spider and Scorpion

## Overview
This project includes two programs: **Spider** and **Scorpion** (subdirs ex00 and ex01).

### Spider /ex00
Downloads all images from a website recursively.  

**Usage:**  
```bash
./spider [-rlp] URL

or in my case 

python spider [-rlp] URL

```
- `-r`: Recursive download.
- `-r -l [N]`: Set maximum recursion depth (default: 5).
- `-p [PATH]`: Save images to specified path (default: `./data/`).

**Supported Formats:** `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`

### Scorpion /ex01
Parses and displays metadata (EXIF, creation date, etc.) of image files.  

**Usage:**  
```bash 
./scorpion FILE1 [FILE2 ...]

or in my case 

python scorpion FILE1 [FILE2 ...]
```

**Supported Formats:** `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`

### Notes
- Avoid using external tools like `wget` or `scrapy`.
- Include all source code and handle errors gracefully.

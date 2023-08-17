# DiskIAnalyser

This is a work-in-progress

It's a simple python script to run on TrueNAS server to analyze the SMART disk reports using ChatGPT.
The goal is to leverage the ChatGPT 3.5 Turbo API to read your disk's SMART reports and generate a simplified report with a health score for each disk. Once the report is generated, it is sent via email.

This script requires the installation of the openai module. If you don't want to use pip, you can follow these steps:

Download the package:
Visit the PyPI page for the module. For openai, the URL is typically:
https://pypi.org/project/openai/

Here you will find tar.gz files for various versions of the module. Download the .tar.gz file that corresponds to the version you want.
Once downloaded, transfer the .tar.gz file to your TrueNAS server (you can use scp or any method of your choice). Once the file is on the server, extract its contents:

<code>tar -xzf openai-x.x.x.tar.gz</code>

After extracting the package, navigate to the package directory and use the setup.py command to install the module:

<code>cd openai-x.x.x
python3 setup.py install</code>

# Result
Here is an example of a report that the script generates : 

<code>


- - - - - - - - - - - - - - 

Disk : da15
Device Model:     ST8000NE001-2M7101
Serial Number:    WSD650SW
Score = 9. The disk is in good health with minimal issues.

- - - - - - - - - - - - - - 

Disk : da12
Device Model:     ST8000NE001-2M7101
Serial Number:    WRD0C326
Score = 8. Disk is in good health with minimal issues.

- - - - - - - - - - - - - - 

Disk : da20
Model Family:     Crucial/Micron Client SSDs
Device Model:     CT2000MX500SSD1
Serial Number:    2205E605B526
Score = 10

- - - - - - - - - - - - - - 

Disk : da2
Device Model:     ST8000NE001-2M7101
Serial Number:    WSD87089
Score = 8. The disk is in good health with minimal issues detected.

- - - - - - - - - - - - - - 

Disk : da5
Device Model:     ST8000NE001-2M7101
Serial Number:    WSD7D2HR
Score = 9. Disk is in good health with only minor issues.

- - - - - - - - - - - - - - 

Disk : da21
Model Family:     Crucial/Micron Client SSDs
Device Model:     CT2000MX500SSD1
Serial Number:    2205E605CB7A
Score = 10

- - - - - - - - - - - - - - 

Disk : da13
Device Model:     ST8000NE001-2M7101
Serial Number:    WSD7MSND
Score = 9

The disk is in good health, with a low number of errors.

- - - - - - - - - - - - - - 

Disk : da14
Device Model:     ST8000NE001-2M7101
Serial Number:    WSD7QN8T
Score = 10. Disk is in perfect health.

- - - - - - - - - - - - - - 

Disk : da4
Device Model:     ST8000NE001-2M7101
Serial Number:    WSD79QBQ
Score = 8. Disk appears to be in good health with few issues.

- - - - - - - - - - - - - - 

Disk : da3
Device Model:     ST8000NE001-2M7101
Serial Number:    WSD870JH
Score = 9. The disk is in good health with minimal issues.

- - - - - - - - - - - - - - 

Disk : da9
Model Family:     Seagate IronWolf Pro
Device Model:     ST8000NE0004-1ZF11G
Serial Number:    ZA2BVPVX
Score = 6. The disk has some worrisome attributes like Raw_Read_Error_Rate and Seek_Error_Rate.

- - - - - - - - - - - - - - 

Disk : da0
Device Model:     ST8000NE001-2M7101
Serial Number:    WSD86ZXD
Score = 9.5. Disk is in good health with minor issues detected.

- - - - - - - - - - - - - - 

Disk : da7
Model Family:     Seagate IronWolf Pro
Device Model:     ST8000NE0004-1ZF11G
Serial Number:    ZA2BLW8T
Score = 9
Disk is in good health.

- - - - - - - - - - - - - - 

Disk : da25
Model Family:     Crucial/Micron Client SSDs
Device Model:     CT2000MX500SSD1
Serial Number:    2205E605B29F
Score = 10. The disk is in perfect health.

- - - - - - - - - - - - - - 

Disk : da22
Model Family:     Crucial/Micron Client SSDs
Device Model:     CT240BX500SSD1
Serial Number:    2212E61F7394
Score = 10. The disk is in perfect health.

- - - - - - - - - - - - - - 

Disk : da19
Model Family:     Crucial/Micron Client SSDs
Device Model:     CT2000MX500SSD1
Serial Number:    2205E605B2AA
Score = 10

- - - - - - - - - - - - - - 

Disk : da17
Device Model:     ST8000NE001-2M7101
Serial Number:    WRD0C2ZX
Score = 8. 
The disk seems to be in good health with only minor issues.

- - - - - - - - - - - - - - 

Disk : da10
Model Family:     Seagate IronWolf Pro
Device Model:     ST8000NE0004-1ZF11G
Serial Number:    ZA29PF0M
Score = 8. Disk is in good health with minor issues detected.

- - - - - - - - - - - - - - 

Disk : da6
Model Family:     Seagate IronWolf Pro
Device Model:     ST8000NE0004-1ZF11G
Serial Number:    ZA29JE08
Score = 8. The disk is in good health with a few minor issues.

- - - - - - - - - - - - - - 

Disk : da1
Device Model:     ST8000NE001-2M7101
Serial Number:    WSD870KF
Score = 9. The disk appears to be in good health with no significant issues.

- - - - - - - - - - - - - - 

Disk : da8
Device Model:     ST8000NE001-2M7101
Serial Number:    WRD0H8Y4
Score = 9. Disk is in very good health, with no major issues detected.

- - - - - - - - - - - - - - 

Disk : da11
Device Model:     ST8000NE001-2M7101
Serial Number:    WRD0C2YC
Score = 10. The disk is in perfect health.

- - - - - - - - - - - - - - 

Disk : da16
Device Model:     ST8000NE001-2M7101
Serial Number:    WSD7QN9F
Score = 9. Disk is in good health with minimal issues detected.

- - - - - - - - - - - - - - 

Disk : da18
Model Family:     Crucial/Micron Client SSDs
Device Model:     CT2000MX500SSD1
Serial Number:    2205E605B607
Score = 10

- - - - - - - - - - - - - - 

Disk : da23
Model Family:     Crucial/Micron Client SSDs
Device Model:     CT240BX500SSD1
Serial Number:    2212E61F74E6
Score = 10. The disk is in perfect health.

- - - - - - - - - - - - - - 

Disk : da24
Model Family:     Crucial/Micron Client SSDs
Device Model:     CT2000MX500SSD1
Serial Number:    2205E605CB7C
Score = 10. The disk is in perfect health.

</code>


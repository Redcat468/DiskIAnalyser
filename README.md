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

You will need an openai API key.

You need to edit the script to set the variables at the begining of the script.



# Result
Here is an example of a report that the script generates : 

```
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

```


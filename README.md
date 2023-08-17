# DiskIAnalyser

This is a work-in-progress

A simple python script to run on TrueNAS server to analyze the SMART disk reports using ChatGPT.
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

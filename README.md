CBRS Tools
----------

This repo has tools used by a CBRS Certified Professional Installer (CPI) to register
CBSDs with a SAS system.  

cpisign.py is used to generate signature data that the CBSD will present to a SAS for CPI signed single-step registration.  


Code Prerequisites
----------

- Python 3.11 (https://python.org/downloads/release/python-3117/)
- pip (https://pip.pypa.io/en/stable/installing/)
- `pip install -r requirement.txt`


cpisign.py Usage:
----------

- Update the parameters in the ***example.json*** file to match your CBSD installation parameters as well as your *cpiId* and *cpiName* and save it as a unique ***file.json***
- For easier usage, move a copy of your *CPI.p12* certificate to the same local directory as this script
- You can generate signature data for multiple CBSDs at a time by having a unique ***file.json*** for each CBSD you are wanting to register
- Have your CPI certificate.p12 password handy. You will be asked to paste it in once you execute the below script
- Execute the script using the following:  
`python3 cpisign.py -k <your_certificate.p12> <file_1.json> ... <file_24.json>`


standalone_cpisign.py Usage:
----------

You can run `standalone_cpisign.py` from the terminal just like `cpisign.py`.
- For easier usage, move a copy of your *CPI.p12* certificate to the same local directory as this script
- You can generate signature data for multiple CBSDs at a time by having a unique ***file.json*** for each CBSD you are wanting to register
- Have your CPI certificate.p12 password handy. You will be asked to paste it in once you execute the below script
- Execute the script using the following:  
`python3 standalone_cpisign.py -k <your_certificate.p12> <file_1.json> ... <file_24.json.json>`
The difference here is that tk is used to select the certificate.p12 and the JSON files in a pop-up dialogue.


Releases Usage:
----------

There are currently two releases attached to this repository. These are standalone executables of `standalone_cpisign.py`.  
Leveraging these executable will allow you to use this script without installing anything additional including setting up a Python environment or IDE.  
I have provided a version built and for use in Windows 11 as well as Mac OS 14.6. They have been tested in these environments have have worked for me. I make no guarantees that they will work for you.  
You can create these executables yourself using [`PyInstaller`](https://pyinstaller.org/en/stable/)  
- `pyinstaller --onefile standalone_cpisign.py`  *Additional usage of PyInstaller is out of scope for this README*

CBRS Tools
----------

This repo has tools used by a CBRS Certified Professional Installer (CPI) to register
CBSDs with a SAS system.  

cpisign.py is used to generate signature data that the CBSD will present to a SAS for CPI signed single-step registration.  


Code Prerequisites
----------

- Python 3.11 (https://python.org/downloads/release/python-3117/)
- pip (https://pip.pypa.io/en/stable/installing/)



cpisign.py Usage:
----------

- Install all requirements using `pip install -r requirements.txt`
- Update the parameters in the ***example.json*** file to match your CBSD installation parameters as well as your *cpiId* and *cpiName* and save it as a unique ***file.json***
- For easier usage, move a copy of your *CPI.p12* certificate to the same local directory as this script
- You can generate signature data for multiple CBSDs as a time by having a unique ***file.json*** for each CBSD you are wanting to register
- Have your CPI certificate.p12 handy. You will be asked to paste it in once you execute the below script
- Execute the script using the following:  
`python3 cpisign.py -k <name_of_your_certificate.p12> <file_1.json> <additional_files_as_needed.json>`


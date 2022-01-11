#! /usr/bin/python
"""
cbrs_backup.py

a tool to download log file from target eNB devices
"""

# SPDX-FileCopyrightText: © 2022 Open Networking Foundation <support@opennetworking.org>
# SPDX-License-Identifier: Apache-2.0

import argparse
import base64
import datetime
import requests
from lxml import etree

parser = argparse.ArgumentParser()
parser.add_argument("address", help="eNB IP address", type=str)
parser.add_argument(
    "-u", "--username", help="eNB UI login username", type=bytes, default=b"sc_femto"
)
parser.add_argument(
    "-p", "--password", help="eNB UI login password", type=bytes, default=b"scHt3pp"
)
args = parser.parse_args()

ENB_DOMAIN = f"https://{args.address}/"
CGI_URL = ENB_DOMAIN + "setup.cgi"

USERNAME = args.username
PASSWORD = args.password

# Disable SSL verification since we signed the certificate by our own
session = requests.session()
session.verify = False

# The login payload passed to cgi gateway
login_payload = {
    "un": base64.b64encode(USERNAME).decode(),
    "pw": base64.b64encode(PASSWORD).decode(),
    "this_file": "logon.htm",
    "next_file": "status.htm",
    "todo": "login",
}

r = session.post(CGI_URL, data=login_payload)
e = etree.HTML(r.text)

serial_number = e.xpath("//td")[4].text

download_payload = {
    "this_file": "logsave.htm",
    "next_file": "logsave.htm",
    "todo": "logdownLoad",
}

with session.post(CGI_URL, data=download_payload, stream=True) as r:
    r.raise_for_status()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{serial_number}_{timestamp}_binary.zip"

    with open(filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"{filename} log backup at {timestamp}.")


text_download_payload = {
    "this_file": "logsave.htm",
    "next_file": "logsave.htm",
    "todo": "TxtlogdownLoad",
}

with session.post(CGI_URL, data=text_download_payload, stream=True) as r:
    r.raise_for_status()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{serial_number}_{timestamp}_text.zip"

    with open(filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"{filename} log backup at {timestamp}.")

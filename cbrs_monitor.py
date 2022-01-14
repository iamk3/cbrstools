#! /usr/bin/python

# SPDX-FileCopyrightText: © 2022 Open Networking Foundation <support@opennetworking.org>
# SPDX-License-Identifier: Apache-2.0

"""
cbrs_configure.py

a tool to configure target eNB devices
"""

import time
import argparse
import base64
import datetime
import requests
from lxml import etree


def timestamp():
    """ replace with logger eventually """
    return datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")


parser = argparse.ArgumentParser()
parser.add_argument("address", help="eNB IP address", type=str)
parser.add_argument(
    "-u", "--username", help="eNB UI login username", type=str, default="sc_femto"
)
parser.add_argument(
    "-p", "--password", help="eNB UI login password", type=str, default="scHt3pp"
)
parser.add_argument(
    "-d", "--delay", help="delay in seconds beetween checks", type=int, default=60
)
parser.add_argument(
    "-c",
    "--count",
    help="number of checks before sending reboot",
    type=int,
    default=10,
)


args = parser.parse_args()

ENB_DOMAIN = f"https://{args.address}/"
CGI_URL = ENB_DOMAIN + "setup.cgi"
LTESTATE_URL = ENB_DOMAIN + "LTE_status.htm"

USERNAME = bytes(args.username.encode())
PASSWORD = bytes(args.password.encode())

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

while True:
    try:
        r = session.post(CGI_URL, data=login_payload, timeout=2)
        e = etree.HTML(r.text)
        serial_number = e.xpath("//td")[4].text
    except requests.exceptions.ConnectTimeout:
        print(f"{timestamp()} Unable to connect {ENB_DOMAIN}, wait 10 seconds.")
        time.sleep(10)
        continue
    except IndexError:
        print(f"{timestamp()} Invalid XML returned from {CGI_URL}, wait 10 seconds.")
        time.sleep(10)
        continue

    cell_down_counter = 0

    while True:
        r = session.get(LTESTATE_URL)
        if r.status_code != 200:
            print(f"{timestamp()} Unable to load {LTESTATE_URL}, retry login.")
            time.sleep(2)
            break

        # try to parse XML, and cache any errors
        cell_state = "BadXML"
        try:
            e = etree.HTML(r.text)
            cell_state = e.xpath("//td")[23].text
        except IndexError:
            print(f"{timestamp()} Invalid XML returned from {LTESTATE_URL}")

        print(f"{timestamp()} Current cell state: {cell_state}")

        # check i
        if cell_state == "Down":
            cell_down_counter = cell_down_counter + 1
        else:
            cell_down_counter = 0

        # eNB is down for too long
        if cell_down_counter > args.count:
            cell_down_total = args.count * args.delay
            print(
                f" {timestamp()} Cell down reaches {cell_down_total}s, restart eNodeB."
            )
            reboot_payload = {
                "this_file": "status.htm",
                "next_file": "status.htm",
                "todo": "reboot",
            }
            session.post(CGI_URL, data=reboot_payload)

            # allow time for the eNB to restart itself
            print(
                f" {timestamp()} Waiting {cell_down_total} after eNodeB restart for recovery"
            )
            time.sleep(cell_down_total)
            break

        time.sleep(args.delay)

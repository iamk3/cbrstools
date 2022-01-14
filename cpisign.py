#!/usr/bin/env python3
"""
cpisign.py

Utility for signing CPI data
"""

# SPDX-FileCopyrightText: © 2021 Open Networking Foundation <support@opennetworking.org>
# SPDX-License-Identifier: Apache-2.0

import os
import json
import getpass
import argparse
from jose import jws

from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives import serialization

parser = argparse.ArgumentParser(description="CBSD CPI signature data generator")
parser.add_argument("-k", "--key", help="The file name of CPI key")
parser.add_argument(
    "signFiles",
    type=str,
    nargs="+",
    help="The file name of sigature data, can accept multiple files in a time.",
)
args = parser.parse_args()

if __name__ == "__main__":
    # get password
    cpi_password = bytes(
        getpass.getpass(prompt="Password for CPI Key %s: " % args.key), "ascii"
    )

    with open(args.key, "rb") as key_file:
        (pkey, cert, addl_cert) = pkcs12.load_key_and_certificates(
            key_file.read(), cpi_password
        )

    pkey_raw = pkey.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )

    if not os.path.exists("output"):
        os.makedirs("output")

    for signFile in args.signFiles:
        with open(signFile, "r") as inFile:
            inFileJson = json.loads(inFile.read())
            # The output is 3 parameters concat with dot to a string
            # 3 params are: protectedHeader, encodedCpiSignedData, digitalSignature
            SIGNED = jws.sign(inFileJson, pkey_raw, algorithm="RS256")

        print(f"* {inFileJson['cbsdSerialNumber']} data was signed")
        with open(f"output/{signFile}.signed", "w") as out_file:
            out_file.write(SIGNED)

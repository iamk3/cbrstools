#!/usr/bin/env python3
"""
cpisign.py

Utility for signing CPI data with key and signature file selection through pop-up dialogs.
Outputs signed data to 'signed_cbsds.txt', appending if the file already exists.
"""

# SPDX-FileCopyrightText: © 2021 Open Networking Foundation <support@opennetworking.org>
# SPDX-License-Identifier: Apache-2.0

import os
import json
import getpass
import argparse
import sys
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askopenfilenames
from jose import jws
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives import serialization


# Initialize Tkinter and hide the root window
root = Tk()
root.withdraw()

# Argument parser for command-line arguments
parser = argparse.ArgumentParser(description="CBSD CPI signature data generator")
parser.add_argument("-k", "--key", help="The file name of CPI key")
parser.add_argument(
    "signFiles",
    type=str,
    nargs="*",
    help="The file name of signature data, can accept multiple files at a time.",
)
args = parser.parse_args()

if __name__ == "__main__":
    # If the key file is not provided, open file dialog to select the key file
    if not args.key:
        print("Please select the CPI key file:")
        args.key = askopenfilename(
            title="Select CPI Key File",
            filetypes=[("PKCS12 files", "*.pfx *.p12"), ("All files", "*.*")],
        )

    # Check if the user selected a file
    if not args.key:
        print("No key file selected. Exiting...")
        sys.exit(1)

    # Get password for the selected CPI key
    cpi_password = bytes(
        getpass.getpass(prompt=f"Password for CPI Key {args.key}: "), "ascii"
    )

    # Load the key and certificates from the PKCS12 file
    with open(args.key, "rb") as key_file:
        (pkey, cert, addl_cert) = pkcs12.load_key_and_certificates(
            key_file.read(), cpi_password
        )

    # Serialize the private key into PEM format
    pkey_raw = pkey.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )

    # If sign files are not provided, open file dialog to select files
    if not args.signFiles:
        print("Please select the signature data files:")
        args.signFiles = askopenfilenames(
            title="Select Signature Data Files",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

    # Check if the user selected files
    if not args.signFiles:
        print("No signature files selected. Exiting...")
        sys.exit(1)

    # Create or append to 'signed_cbsds.txt'
    with open("signed_cbsds.txt", "a") as output_file:
        # Iterate over each input file to sign
        for signFile in args.signFiles:
            with open(signFile, "r") as inFile:
                inFileJson = json.loads(inFile.read())
                # The output is 3 parameters concatenated with a dot into a string
                # The parameters are: protectedHeader, encodedCpiSignedData, digitalSignature
                SIGNED = jws.sign(inFileJson, pkey_raw, algorithm="RS256")

            # Log the signed data
            output_file.write(f"File: {os.path.basename(signFile)}\n")
            output_file.write(f"CBSD Serial Number: {inFileJson['cbsdSerialNumber']}\n")
            output_file.write(f"Signed Data: {SIGNED}\n\n")

            # Print confirmation for each file signed
            print(f"* {inFileJson['cbsdSerialNumber']} data was signed and written to 'signed_cbsds.txt'")

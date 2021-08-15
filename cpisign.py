#!/usr/bin/env python3
"""
cpisign.py

Utility for signing CPI data
"""

# SPDX-FileCopyrightText: © 2021 Open Networking Foundation <support@opennetworking.org>
# SPDX-License-Identifier: Apache-2.0

import getpass
from jose import jws

from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives import serialization

CPI_KEY_PATH = "./YOUR_CPI_KEY.p12"

cpiSignedData = {
    "fccId": "P27-SCE4255W",
    "cbsdSerialNumber": "2009CW5000016",
    "installationParam": {
        "latitude": 32.344752,
        "longitude": -111.012302,
        "height": 1,
        "heightType": "AGL",
        "indoorDeployment": True,
    },
    "professionalInstallerData": {
        "cpiId": "GOOG-001212",
        "cpiName": "Wei-Yu Chen",
        "installCertificationTime": "2021-08-14T00:00:00Z",
    },
}

# get password
cpi_password = bytes(getpass.getpass(), "ascii")

with open(CPI_KEY_PATH, "rb") as key_file:
    (pkey, cert, addl_cert) = pkcs12.load_key_and_certificates(
        key_file.read(), cpi_password
    )

pkey_raw = pkey.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption(),
)

(protectedHeader, encodedCpiSignedData, digitalSignature) = jws.sign(
    cpiSignedData, pkey_raw, algorithm="RS256"
).split(".")

print(protectedHeader)
print(encodedCpiSignedData)
print(digitalSignature)

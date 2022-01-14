#!/usr/bin/env bash

# SPDX-FileCopyrightText: © 2021 Open Networking Foundation <support@opennetworking.org>
# SPDX-License-Identifier: Apache-2.0

# list of eNB IP addresses, space separated
enb_ips=( 10.0.0.10 10.0.0.11 )

# credentials for eNB - currently ignored
enb_user="sc_femto"
enb_pass="scHt3pp"

# delay in seconds
delay_s=3600

# create directories if they dont already exist
for logdir in "${enb_ips[@]}"
do
  mkdir -p "$logdir"
done

# activate virtualenv
. venv_cbrs/bin/activate

# kill certificate warning
export PYTHONWARNINGS="ignore:Unverified HTTPS request"

# run logging script in loop forever
while true
do

# make backups
for ip in "${enb_ips[@]}"
do
  python cbrs_backup.py -u "$enb_user" -p "$enb_pass" "$ip" | tee -a "${ip}_backup.log"
done

# delay until next run
sleep $delay_s

done

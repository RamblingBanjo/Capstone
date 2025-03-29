#!/bin/bash

cd /home/radiosonde/HABAP

source meshtastic-env/bin/activate
python3 meshtastic_script.py
deactivate

#!/bin/bash

# Remove existing GeoLite files
rm -rf geolite

# Fetch current data
wget https://geolite.maxmind.com/download/geoip/database/GeoLite2-City-CSV.zip

# Unzip and arrange files
unzip GeoLite2-City-CSV.zip -d geolite
cd geolite && mv GeoLite2-City-CSV_*/* . && cd .. && rm GeoLite2-City-CSV.zip

# Run data loading script
python3 swagger_server/load_data.py

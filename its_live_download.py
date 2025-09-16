#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 12:10:38 2023

@author: student
"""

import os
import requests

# Read the text file containing URLs
with open('/Users/rishi/Desktop/Pine Island/ITS_LIVE velocity mosaics/batch_1.txt', 'r') as file:
    urls = file.readlines()

# Remove whitespace and newlines from each URL
urls = [url.strip() for url in urls]

# Download the files only if they don't already exist
for url in urls:
    filename = url.split('/')[-1]  # Extract the filename from the URL
    if os.path.exists(filename):
        print(f"Skipping (already exists): {filename}")
        continue
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download: {filename}")

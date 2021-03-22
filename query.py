#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import json
import os
import sys
import urllib.parse

import pandas as pd
import requests

API_URL = 'https://api.dehashed.com/search?query='
API_EMAIL = os.getenv('DEHASHED_EMAIL')
API_TOKEN = os.getenv('DEHASHED_TOKEN')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception("Insufficient number of parameter.")

    data = []
    with open(sys.argv[1]) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            data.append(row)

    results = []
    for entry in data:
        if entry['Email-Addresse'] is not None:
            print(entry['Email-Addresse'])
 
            r = requests.get(API_URL + 'email:' + urllib.parse.quote_plus(entry['Email-Addresse']), auth=(API_EMAIL, API_TOKEN), headers={'accept': 'application/json'})
            response = r.json()

            if response['total'] > 0:
                for result in response['entries']:
                    results.append(result)
        
        if entry['Name'] is not None and entry['Vorname'] is not None:
            name = r'"' + entry['Vorname'].split(' ')[0] + " " + entry['Name'] + r'"'
            print(name)
            
            r = requests.get(API_URL + 'email:' + urllib.parse.quote_plus(name), auth=(API_EMAIL, API_TOKEN), headers={'accept': 'application/json'})
            response = r.json()
            
            if response['total'] > 0:
                for result in response['entries']:
                    results.append(result)

        if entry['Telefon-Nummer'] is not None:
            phone = entry['Telefon-Nummer'].replace(' ','')
            print(phone)
            
            r = requests.get(API_URL + 'phone:' + urllib.parse.quote_plus(phone), auth=(API_EMAIL, API_TOKEN), headers={'accept': 'application/json'})
            response = r.json()
            
            if response['total'] > 0:
                for result in response['entries']:
                    results.append(result)

    table = pd.DataFrame.from_dict(results)
    print(table)
    table.to_csv('result.csv', index=False, header=True)

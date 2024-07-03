# -*- coding: utf-8 -*-
"""
Created on Fri May 17 13:29:46 2024

@author: TESTER
"""

import json
import requests
import subprocess
import glob
import numpy as np
import re
import matplotlib.pyplot as plt
import argparse
import time

def qmean6(pdb_file, out_file):
    print(pdb_file)
    # Define the QMEAN submission URL
    qmean_url = "https://swissmodel.expasy.org/qmean/submit/"

    # Send the POST request with the file and email
    for attempt in range(5):
        try:
            response = requests.post(
                url=qmean_url,
                data={
                    "email": "montse.romagosa@irbbarcelona.org"
                },
                files={
                    "structure": open(pdb_file, 'rb')
                }
            )

            # Check if the response status code is 200 (OK)
            if response.status_code == 200:
                # Print the JSON response in a formatted manner
                response_data = response.json()
                print(json.dumps(response_data, indent=4, sort_keys=True))
            else:
                print(f"Failed to submit the file. Status code: {response.status_code}")
                response.raise_for_status()

            status=''
            while not status=="COMPLETED":
                # Retrieve the URL to check the results
                results_url = response_data.get("results_json")
                
                if results_url:
                    # Send a GET request to the results URL
                    current_status_response = requests.get(results_url)
                
                    # Check if the response status code is 200 (OK)
                    if current_status_response.status_code == 200:
                        # Parse the JSON response from the GET request
                        current_status_data = current_status_response.json()
                        
                        # Print the entire JSON data in a formatted manner
                        print(json.dumps(current_status_data, indent=4, sort_keys=True))
                
                        # Extract and print the 'status' key
                        status = current_status_data.get("status", "Status not found")
                        print(f"Status: {status}")
                    else:
                        print(f"Failed to get the current status. Status code: {current_status_response.status_code}")
                        current_status_response.raise_for_status()
                else:
                    print("The key 'results_json' is missing or empty in the initial response.")
                #rest to avoid spend all the permited requests
                time.sleep(15)

            current_status = requests.get(response.json()["results_json"])

            print(json.dumps(current_status.json(), indent=4, sort_keys=True))

            #extract the qmean6 value    
            qmean6 = current_status_data["models"]["model_001"]["scores"]["global_scores"]["qmean6_norm_score"]
            print(f"qmean6: {qmean6}")

            #write the qmean6 value corresponding to each pdb file
            quality_file=open(out_file, 'a')
            quality_file.write(pdb_file + ' ' + str(qmean6) + '\n')
            continue
        except Exception as err:
            print(f"An error occurred: {err}")
            break

#Ask for required arguments
parser=argparse.ArgumentParser(description='Program description')

parser.add_argument('--path_AF', required='True', help='Path of the PDB files')
parser.add_argument('--out_file', required='True', help='File name of the output')
args=parser.parse_args()

path_to_AF=args.path_AF
out_file=args.out_file

#check the qmean6 vaule for all the structures
pdb_files = glob.glob(path_to_AF + '/*.pdb')
print(len(pdb_files))
for file in pdb_files:
    qmean6(file, out_file)

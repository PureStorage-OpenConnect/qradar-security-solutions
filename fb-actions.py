import urllib3
import datetime
import argparse
import sys
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import os
import platform

# Disable InsecureRequestWarning from urllib3 
# Suppress the warning about insecure requests (only use this for testing purposes)
urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


USER_AGENT_BASE = 'QRadar-Integration'
VERSION = 'v1.0'
user_agent = "%(base)s %(class)s/%(version)s (%(platform)s)" % {
            "base": USER_AGENT_BASE,
            "class": __name__,
            "version": VERSION,
            "platform": platform.platform(),
        }


# Function to create a filesystem snapshot
def create_fs_snapshot(array_name, filesystem_name, xAuthToken, request_body=None):
    print xAuthToken
    api_url = 'https://' + array_name + '/api/' + apiVersion + '/file-system-snapshots?source_names=' + filesystem_name

    try:
        # Make a POST request to the API endpoint
        response = requests.post(api_url, headers={'x-auth-token': xAuthToken, 'User-agent': user_agent}, json=request_body, verify=False)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Print the response content (you may want to process this differently based on your use case)
            print "API Response:"
            print response.json()
        else:
            # Print an error message if the request was not successful
            #print "Error: {response.status_code} - {response.text}")
            print "Error: {} - {}".format(response.status_code, response.text)

    except requests.RequestException as e:
        # Handle exceptions related to the request, such as network errors
        print "Request Exception: {}".format(e)

    except Exception as e:
        # Handle other unexpected exceptions
        print "An unexpected error occurred {}".format(e)


        

# main function

if __name__ == "__main__":
    # Argument parser
    parser = argparse.ArgumentParser(description="Program to create filesystem snapshot on FlashBlade ")
    subparser = parser.add_subparsers(dest='command')
    fssnap = subparser.add_parser('fs_snapshot')
    fssnap.add_argument("array_name", help="FlashBlade IP")
    fssnap.add_argument("filesystem_name", help="filesystem name")

    mfssnap = subparser.add_parser('multifs_snapshot')
    mfssnap.add_argument("array_name", help="FlashBlade IP")

    try:
        options = parser.parse_args()
    except Exception as e:
        parser.print_help()
        sys.exit(1)

    config = {}
    with open('pure.conf') as fh:
        for line in fh:
            data = line.split(':')
            array = data[0]
            arrayinfo = data[1:]
            config[array] = arrayinfo

    array_name = options.array_name
    
    if array_name in config:
        api_token = config[array_name][0]
        fslist = config[array_name][1].split(',')
        print fslist
        print api_token
        
        
        if not fslist:
            print "Filesystem list for this FB missing in the configuration."
        
        url = 'https://' + array_name + '/api/api_version'

        res = requests.get(url, verify=False)
        apiVersion = res.json().get('versions')[-1]

        print apiVersion
        url = 'https://' + array_name + '/api/login'

        try:
            # Make a POST request to the API endpoint
            response = requests.post(url, headers={'api-token': api_token, 'User-agent': user_agent}, verify=False)
            print(response.status_code)
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Print the response content (you may want to process this differently based on your use case)
                print "API Response:"
                print response.json()
                xAuthToken = response.headers.get('x-auth-token')

                now = datetime.datetime.now()
                suffix = "qradar-" + now.strftime("%Y-%m-%d-%H-%M-%S")

                request_body = {
                    "suffix": suffix
                }


                # Single filesystem Snapshot action
                if options.command == "fs_snapshot":
                    print "action - fs_snapshot"
                    create_fs_snapshot(array_name, options.filesystem_name, xAuthToken, request_body)

                
                # multiple filesystem Snapshot action
                elif options.command == "multifs_snapshot":
                    print "action - multifs_snapshot"
                    for filesystem in fslist:
                        create_fs_snapshot(array_name, filesystem, xAuthToken, request_body)

            else:
                # Print an error message if the request was not successful
                #print "Error: {response.status_code} - {response.text}")
                print "Error: {} - {}".format(response.status_code, response.text)

        except requests.RequestException as e:
            # Handle exceptions related to the request, such as network errors
            print "Request Exception: {}".format(e)

        except Exception as e:
            # Handle other unexpected exceptions
            print "An unexpected error occurred {}".format(e)
    else:
        print "Config section for this FA not found in the configuration."
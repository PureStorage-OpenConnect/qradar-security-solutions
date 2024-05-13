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


# Function to create a  PG snapshot
def create_pg_snapshot(array_name, pg_name, xAuthToken, request_body=None):

    api_url = 'https://' + array_name + '/api/' + apiVersion + '/protection-group-snapshots?source_names=' + pg_name

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
        

# Function to create a volume snapshot
def create_vol_snapshot(array_name, volume_name, xAuthToken, request_body=None):
    print xAuthToken
    api_url = 'https://' + array_name + '/api/' + apiVersion + '/volume-snapshots?source_names=' + volume_name

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


# Function to create a  PG snapshot
def remove_user(array_name, user_name,xAuthToken):

    api_url = 'https://' + array_name + '/api/' + apiVersion + '/admins?names=' + user_name

    try:
        # Make a POST request to the API endpoint
        response = requests.delete(api_url, headers={'x-auth-token': xAuthToken, 'User-agent': user_agent}, json=request_body, verify=False)

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
    parser = argparse.ArgumentParser(description="Program to create Protection Group snapshot on FlashArray ")
    subparser = parser.add_subparsers(dest='command')
    pgsnap = subparser.add_parser('pg_snapshot')
    pgsnap.add_argument("array_name", help="FlashArray IP")

    volsnap = subparser.add_parser('vol_snapshot')
    volsnap.add_argument("array_name", help="FlashArray IP")
    volsnap.add_argument("volume_name", help="Volume name")

    mvolsnap = subparser.add_parser('multivol_snapshot')
    mvolsnap.add_argument("array_name", help="FlashArray IP")

    uremove = subparser.add_parser('remove_user')
    uremove.add_argument("array_name", help="FlashArray IP")
    uremove.add_argument("user_name", help="User name")
    
    try:
        options = parser.parse_args()
    except Exception as e:
        parser.print_help()
        sys.exit(1)

    config = {}
    with open('/opt/qradar/bin/ca_jail/pure.conf') as fh:
        for line in fh:
            data = line.split(':')
            array = data[0]
            arrayinfo = data[1:]
            config[array] = arrayinfo

    array_name = options.array_name
    
    if array_name in config:
        api_token = config[array_name][0]
        vollist = config[array_name][1].split(',')
        pglist = config[array_name][2].split(',')
        print vollist
        print pglist
        
        if not vollist:
            print "Volume list for this FA missing in the configuration."
        if not pglist:
            print "Protection Group list for this FA missing in the configuration."

        url = 'https://' + array_name + '/api/api_version'

        res = requests.get(url, verify=False)
        apiVersion = res.json().get('version')[-1]

        print apiVersion
        url = 'https://' + array_name + '/api/' + apiVersion + '/login'

        try:
                # Make a POST request to the API endpoint
                response = requests.post(url, headers={'api-token': api_token, 'User-agent': user_agent}, verify=False)

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

                    # PG Snapshot action
                    if options.command == 'pg_snapshot':
                        print "action - pg_snapshot"
                        for pg in pglist:
                            create_pg_snapshot(array_name,pg,xAuthToken,request_body)


                    # Single volme Snapshot action
                    elif options.command == "vol_snapshot":
                        print "action - vol_snapshot"
                        create_vol_snapshot(array_name,options.volume_name, xAuthToken, request_body)

                    
                    # multiple volmes Snapshot action
                    elif options.command == "multivol_snapshot":
                        print "action - multivol_snapshot"
                        for volume in vollist:
                            create_vol_snapshot(array_name,volume,xAuthToken,request_body)

                    # User remove action

                    elif options.command == "remove_user":
                        print "action - remove_user"
                        remove_user(array_name,options.user_name,xAuthToken)
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




#!/usr/bin/env python3

import sys
import argparse
from requests import get
from transip_rest_client import TransipRestClient

def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="DynDNS: Updates a DNS record for a dynamic IP address.")
    parser.add_argument("-u", "--user", help="Your username.", required=True)
    parser.add_argument("-k", "--key", help="Key file containing RSA private key.", required=True)
    parser.add_argument("-n", "--name", help="Name of the record (e.g. 'www').", required=True)
    parser.add_argument("-d", "--domain", help="Existing DNS domain (e.g. 'example.com').", required=True)
    parser.add_argument("-v", "--verbose", action='store_true', help="Verbose mode.")

    options = parser.parse_args(args)
    return options

def find(arr , id):
    for x in arr:
        if x["name"] == id:
            return x

def main(key, username, domain, name, verbose):
    with open(key, 'r') as f:
        my_RSA_key = f.read()

    if "BEGIN RSA PRIVATE KEY" not in my_RSA_key:
        print("Key in incorrect format, convert the key with the following command:")
        print("openssl rsa -in privatekey.txt -out rsaprivatekey.txt")
        return

    newIp = get('https://api.ipify.org').text
    if verbose:
        print(f"Retrieved IP from api.ipify.org: {newIp}")
    
    client = TransipRestClient(user=username, rsaprivate_key=my_RSA_key, global_key=True)
    entries = client.get_dns_entries(domain=domain)
    if verbose:
        print(f"Found {len(entries)} DNS entries")

    entry = find(entries, name)

    if entry is None:
        print(f"No ip found, adding {newIp}")
        client.post_dns_entry(domain=domain, name=name, expire=300, record_type='A', content=newIp)
    else:
        oldIp = entry["content"]
        if verbose:
            print(f"Found current IP in DNS entry: {oldIp}")
        
        if oldIp != newIp:
            print(f"Updating {oldIp} to {newIp}")
            client.patch_dns_entry(domain=domain, name=name, record_type='A', content=newIp)
        else:
            print(f"Not updating {oldIp}")

if __name__ == "__main__":
    options = getOptions()

    if options.verbose:
        print("Verbose output enabled.")

    main(options.key, options.user, options.domain, options.name, options.verbose)

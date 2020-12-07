TransIP Python 3 DynDNS Client
------------------------------

When you don't have a static IP addres at home, but still want a DNS entry
to make your home network reachable.

This script updates a DNS record at TransIP, with your current IP address.

# Requirements
This script uses the python REST API module for TransIP, which can be found here:
https://github.com/reinoud/transip_rest_client

To get this to work, you should have the following:
 - have an account at TransIP
 - have an domain name at TransIP
 - on the [API page](https://www.transip.nl/cp/account/api/):
   - turn API on 
   - generate a keypair and copy the Private Key that is _shown once_
   - save it in a file called privatekey.txt
 - convert the private key to an RSA private key (you need openssl tools installed):
 ```
 openssl rsa -in privatekey.txt -out rsaprivatekey.txt
 ```

## Usage
For example, when you own the `example.com` domain and you want to have 
`home.example.com` point to your home server. Let's assume your TransIP
username is `myusername`.

Run the `dyndns.py` script as follows:
```
./dyndns.py -u myusername -k rsaprivatekey.txt -n home -d example.com
```

## Notes
I have this script running as a cron job on my server.

When your dynamic IP address changes, it takes some time to update
the DNS records. So your server should be unreachable for a little while.

Using the transip_rest_client, can be as simple as copying the following folder
to the same folder as the `dyndns.py` script resides:
https://github.com/reinoud/transip_rest_client/tree/master/transip_rest_client

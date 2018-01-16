# Instruction
This is how I automatically detect my home IP address change and, update new IP to my DNS server, at the same time, send an email to me.
# Configuration
## File
```
syncip/config.json
```
## Explanation
* ```ipget```
    * ```uri```: Base url of your ipecho server.
    * ```access_token```: Token that added to http request's 'Access-Token' attribute.
* ```file```
    * ```record_file```: File that records current IP address.
* ```mail```
    * ```host_user```: Email sender's login user name.
    * ```host_pwd```: Email sender's login user password.
    * ```to```: Email receiver's address(only receive one email).
    * ```server_host```: Host of sender's mail server.
    * ```server_port```: Port of sender's mail server.
* ```dnspod```
    * ```dp_token```: My DNSPod API's id and access token, separated by ','.
    * ```dp_base```: DNSPod's API base URI, defaultly, 'dnsapi.cn'.
    * ```dp_name```: My DNSPod API's name.
    * ```dp_version```: My DNSPod API's version.
    * ```dp_domain```: Base domain that you will update.
    * ```dp_mail```: My register email on DNSPod.
* ```sub_domain```: Sub domain that the new IP will binded on.
# Run
```bash
sh syncip.sh
```

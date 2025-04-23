# Prisma SD-WAN Base (Preview)
The purpose of the script is to admin up or down a service link based on the service endpoint address. 

#### License
MIT

#### Requirements
* Active Prisma SD-WAN Account - Please generate your API token and add it to prismasase_settings.py
* Python >=3.6

#### Installation:
 Scripts directory. 
 - **Github:** Download files to a local directory, manually run the scripts. 
 - pip install -r requirements.txt

### Examples of usage:
 Please generate your service account and add it to prismasase_settings.py
 
 - ./Tunnel-Down-Site.py -S Home-Office -I 130.41.43.64 -E False
 -- This will bring down a tunnel with peer IP of 130.41.43.64 for a specific site
 - ./Tunnel-Down-Retail.py -I 130.41.43.63 -E True
 -- This will bring up a tunnel with peer IP of 130.41.43.64 for a specific domain 
 
### Caveats and known issues:
 - This is a PREVIEW release, hiccups to be expected. Please file issues on Github for any problems.

#### Version
| Version | Build | Changes |
| ------- | ----- | ------- |
| **1.0.0** | **b1** | Initial Release. |


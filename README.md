# unifi-update-local-dns-record
Python script to connect to UniFi Gateway to update the Local DNS Record of a client device.

This script was originally [posted](https://www.reddit.com/r/UNIFI/s/TgxCym5ssj) on r/UNIFI by u/gelarue. I have made a
few modifications to it:

- Instead of requiring the script to be modified before running, the script will ask for the necessary variables when
  ran.
  - Note: The password input will not be printed as it's being typed.
- Remove unused `SET_VALUE` variable.
- `new_value` variable's input prompt text updated to include an example.
- Added additional print warning a gateway reboot may be needed to apply the DNS record update.

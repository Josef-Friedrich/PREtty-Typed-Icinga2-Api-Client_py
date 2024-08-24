

## <a id="config-file"></a> Config file

You can also specify a config file (in ini format) containing all necessary information.

Example:

    client = Client('https://localhost:5665', config_file='/etc/icinga2api')

The config file looks like:

    [api]
    url = https://icinga2:5665
    certificate = /etc/ssl/certs/myhostname.crt
    key = /etc/ssl/private/myhostname.key
    ca_certificate = /etc/ssl/certs/ca.crt


## <a id="server-verification"></a> Server verification

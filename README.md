# Overview

This is a layered implementation of the `tls:certificates interface` that uses
the requires part of the relation.

# Usage

This is a middle layer and can not be used on its own.

Implementing layers must set certificates-directory in layer options

### Certificate Paths

Layer options are defined for storing the certificates on disk. These layer
options must be defined in your consuming layer. As an example:

```yaml
options:
  tls-client:
    ca_certificate_path: /etc/ssl/myservice/ca.crt
    server_certificate_path: /etc/ssl/myservice/server.crt
    server_key_path: /etc/ssl/myservice/server.key
    client_certificate_path: /etc/ssl/myservice/client.crt
    client_key_path: /etc/ssl/myservice/client.key

```

## To request a certificate

If the layer needs a server certificate it must request one with the relation
code.

```python 
@when('certificates.available')
def send_data(tls):
    '''Send the data that is required to create a server certificate for
    this server.'''
    # Use the public ip of this unit as the Common Name for the certificate.
    common_name = hookenv.unit_public_ip()
    # Get a list of Subject Alt Names for the certificate.
    sans = []
    sans.append(hookenv.unit_public_ip())
    sans.append(hookenv.unit_private_ip())
    sans.append(socket.gethostname())
    # Create a path safe name by removing path characters from the unit name.
    certificate_name = hookenv.local_unit().replace('/', '_')
    tls.request_server_cert(common_name, sans, certificate_name)
```

## Known Limitations and Issues

This is a middle layer that needs to be built into another charm. The
layer must define the certificate_directory layer option before this layer
will place the certificates or keys.

# Contact Information

  - **Maintainer**: Matthew Bruzek &lt;matthew.bruzek@canonical.com&gt;

## Links

  - The [easyrsa charm](https://github.com/juju-solutions/layer-easyrsa)
  

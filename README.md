# Overview

This is a layered implementation of the `tls:certificates interface` that uses
the requires part of the relation.

# Usage

This is a middle layer and can not be used on its own.

## To request a certificate

If the layer needs a server or client certificate it must request one by
calling either `charms.layer.tls_client.request_server_cert` or
`charms.layer.tls_client.request_client_cert`, both of which take the following args:

  * `common_name` Common name (CN), also known as distinguished name (DN),
    for the certificate. This is required. Multiple calls with the same CN
    will be treated as the same certificate (allowing for updates to the
    `sans`).
  * `sans` Optional list of Subject Alternative Names for the certificate.
  * `cert_path` Optional path to write cert data for the ceritifcate.
  * `key_path` Optional path to write key data for the certificate.

The charm should then watch for one of the following flags to be set:

  * `tls_client.certs.saved` When all requested certificates have been
    written to disk at least once. Note that this flag is not updated if the
    certificates have changed, unlike the following flags.
  * `tls_client.certs.changed` When any cert data has changed (and been written
    to disk).
  * `tls_client.server.certs.changed` When any server cert data has changed
    (and been written to disk).
  * `tls_client.server.cert.{common_name}.changed` When a specific server cert
    data has changed (and been written to disk).
  * `tls_client.client.certs.changed` When any client cert data has changed
    (and been written to disk).
  * `tls_client.client.cert.{common_name}.changed` When a specific client cert
    data has changed (and been written to disk).

The changed flags should be removed by the charm layer once handled.

For example:
```python
from charms import layer


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
    layer.tls_client.request_server_cert(common_name, sans,
                                         crt_path='/etc/certs/server.crt',
                                         key_path='/etc/certs/server.key')
```

### Layer Options

The layer supports one option, for specifying a location to write the CA certificate
out to (in addition to installing it at the system level): `ca_certificate_path`

```yaml
options:
  tls-client:
    ca_certificate_path: /etc/ssl/myservice/ca.crt
```

Once the CA certificate has been installed and written, the flag `tls_client.ca.saved`
will be set.

Other layer options for using a single server certificate and single, global
client certificate are now deprecated.

# Contact Information

This layer is maintained by the Kubernetes team at Canonical. Issues can be
filed on the [GitHub repo](https://github.com/juju-solutions/layer-tls-client),
and questions can be asked on [Discourse](https://discourse.jujucharms.com/) or
on IRC in #cdk8s or #juju on Freenode.

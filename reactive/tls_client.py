import os
import socket

from subprocess import check_call

from charms import layer

from charms.reactive import when, when_not, set_state
from charmhelpers.core import hookenv


@when_not('tls-client.certificates.directory')
def get_directory():
    '''Get the layer option of where to put the certificates.'''
    layer_options = layer.options('tls-client')
    if layer_options.get('certificates-directory'):
        set_state('tls-client.certificates.directory')
    else:
        hookenv.status_set('blocked',
                           'Missing certificates_directory layer option.')


@when('certificates.ca.available', 'tls-client.certificates.directory')
def store_ca(tls):
    '''Read the certificate authority from the relation object and install
    the ca on this system.'''
    # Get the CA from the relationship object.
    certificate_authority = tls.get_ca()
    if certificate_authority:
        # Update /etc/ssl/certs and generate ca-certificates.crt
        install_ca(certificate_authority)

        layer_options = layer.options('tls-client')
        # Get the certificate directory from the layer options.
        directory = layer_options.get('certificates-directory')
        if not os.path.isdir(directory):
            os.makedirs(directory)
        destination = os.path.join(directory, 'ca.crt')
        hookenv.log('Writing the CA to {0}'.format(destination))
        with open(destination, 'w') as fp:
            fp.write(certificate_authority)


@when('certificates.server.cert.available')
@when('tls-client.certificates.directory')
def store_server(tls):
    '''Read the server certificate and server key from the relation object
    and save them to the certificate directory..'''
    server_cert, server_key = tls.get_server_cert()
    if server_cert and server_key:
        layer_options = layer.options('tls-client')
        # Get the certificate directory from the layer options.
        directory = layer_options.get('certificates-directory')
        if not os.path.isdir(directory):
            os.makedirs(directory)
        cert_file = os.path.join(directory, 'server.crt')
        hookenv.log('Writing server certificate to {0}'.format(cert_file))
        with open(cert_file, 'w') as stream:
            stream.write(server_cert)
        key_file = os.path.join(directory, 'server.key')
        hookenv.log('Writing server key to {0}'.format(key_file))
        with open(key_file, 'w') as stream:
            stream.write(server_key)


@when('certificates.client.cert.available')
@when('tls-client.certificates.directory')
def store_client(tls):
    '''Read the client certificate and client key from the relation object
    and copy them to the certificate directory.'''
    client_cert, client_key = tls.get_client_cert()
    if client_cert and client_key:
        layer_options = layer.options('tls-client')
        # Get the certificate directory from the layer options.
        directory = layer_options.get('certificates-directory')
        if not os.path.isdir(directory):
            os.makedirs(directory)
        cert_file = os.path.join(directory, 'client.crt')
        hookenv.log('Writing client certificate to {0}'.format(cert_file))
        with open(cert_file, 'w') as stream:
            stream.write(client_cert)
        key_file = os.path.join(directory, 'client.key')
        hookenv.log('Writing client key to {0}'.format(key_file))
        with open(key_file, 'w') as stream:
            stream.write(client_key)


def install_ca(certificate_authority):
    '''Install a certificiate authority on the system by calling the
    update-ca-certificates command.'''
    if certificate_authority:
        name = hookenv.service_name()
        ca_file = '/usr/local/share/ca-certificates/{0}.crt'.format(name)
        hookenv.log('Writing CA to {0}'.format(ca_file))
        # Write the contents of certificate authority to the file.
        with open(ca_file, 'w') as fp:
            fp.write(certificate_authority)
        # Update the trusted CAs on this system.
        check_call(['update-ca-certificates'])
        message = 'Generated ca-certificates.crt for {0}'.format(name)
        hookenv.log(message)

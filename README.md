# Overview

This is a layered implementation of the `tls:certificates interface` that uses
the requires part of the relation.

# Usage

This is a middle layer and can not be used on its own.

Implementing layers must set certificates-directory

## Known Limitations and Issues

This is a middle layer that needs to be built into another charm. The
layer must define the certificate_directory layer option before this layer
will place the certificates or keys.

# Contact Information

  - **Maintainer**: Matthew Bruzek &lt;matthew.bruzek@canonical.com&gt;

## Links

  - The [easyrsa charm](https://github.com/juju-solutions/layer-easyrsa)
  

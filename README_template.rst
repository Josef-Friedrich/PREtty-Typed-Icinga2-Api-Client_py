{{ badge.pypi }}

{{ badge.github_workflow() }}

.. image:: https://readthedocs.org/projects/pretty-typed-icinga2-api-client-py/badge/?version=latest
    :target: https://pretty-typed-icinga2-api-client-py.readthedocs.io
    :alt: Documentation Status

pretiac: PREtty Typed Icinga2 Api Client
========================================

For more information about the project, please read the
`API documentation <https://pretty-typed-icinga2-api-client-py.readthedocs.io>`_.

``pretiac`` stands for **PRE** tty **T** yped **I** cinga2 **A** pi **C** lient.
This project is a fork / extension of the
`TeraIT-at/icinga2apic <https://github.com/TeraIT-at/icinga2apic>`__ api client.
The client class of ``icinga2apic`` was renamed to :class:`pretiac.raw_client.RawClient`.
``pretaic`` provides an additional client (:class:`pretiac.client.Client`), which is typed.
`Pydantic <https://github.com/pydantic/pydantic>`__ is used to validate the
Icinga2 REST API and to convert the JSON
output into Python data types.

Authenticating Icinga 2 API Users with TLS Client Certificates
--------------------------------------------------------------

Source: `Blog post at icinga.com
<https://icinga.com/blog/2022/11/16/authenticating-icinga-2-api-users-with-tls-client-certificates/>`__

Icinga 2 supports a second authentication mechanism: TLS client certificates.
This is a feature of TLS that also allows the client to send a certificate, just
like the server does, allowing the server to authenticate the client as well.

You can start by generating a private key and a certificate signing request
(CSR) with the ``icinga2 pki new-cert`` command:

.. code-block::

    icinga2 pki new-cert \
        --cn my-api-client \
        --key my-api-client.key.pem \
        --csr my-api-client.csr.pem

This writes the key and CSR to the files my-api-client.key.pem and
my-api-client.csr.pem respectively. Note that you can also use other methods to
generate these files. It is only important that the CSR contains a meaningful
common name (CN). This allows you to also generate the private key on a hardware
security token for example.

Next, the CSR has to be signed by the Icinga CA. This can be achieved by copying
the CSR file to the Icinga master and running the following command:

.. code-block::

    icinga2 pki sign-csr \
        --csr my-api-client.csr.pem \
        --cert my-api-client.cert.pem

This generates a certificate, however, so far, Icinga 2 does not know what to do
with this certificate. To fix this, a new ApiUser object has to be created that
connects the certificate and its common name with some permissions.

.. code-block::

    object ApiUser "my-api-client" {
        client_cn = "my-api-client"
        permissions = [ "*" ]
    }

After reloading the Icinga 2 configuration, the certificate is now ready to use.
The following example uses curl, but any HTTPS client that supports client
certificates will do.

Command line interface
----------------------

{{ cli('pretiac --help') | literal }}

``pretiac actions``
^^^^^^^^^^^^^^^^^^^

{{ cli('pretiac actions --help') | literal }}

``pretiac actions send-service-check-result``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

{{ cli('pretiac actions send-service-check-result --help') | literal }}

``pretiac config``
^^^^^^^^^^^^^^^^^^

{{ cli('pretiac config --help') | literal }}

``pretiac config delete``
^^^^^^^^^^^^^^^^^^^^^^^^^

{{ cli('pretiac config delete --help') | literal }}

``pretiac objects``
^^^^^^^^^^^^^^^^^^^

{{ cli('pretiac objects --help') | literal }}

``pretiac objects delete-service``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

{{ cli('pretiac objects delete-service --help') | literal }}

``pretiac objects list``
^^^^^^^^^^^^^^^^^^^^^^^^

{{ cli('pretiac objects list --help') | literal }}

.. image:: http://img.shields.io/pypi/v/pretiac.svg
    :target: https://pypi.org/project/pretiac
    :alt: This package on the Python Package Index

.. image:: https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/actions/workflows/tests.yml
    :alt: Tests

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

:: 

    Usage: pretiac [OPTIONS] COMMAND [ARGS]...

      Command line interface for the Icinga2 API.

    Options:
      -d, --debug  Increase debug verbosity (use up to 3 times): -d: info -dd:
                   debug -ddd: verbose.
      --help       Show this message and exit.

    Commands:
      actions      There are several actions available for Icinga 2 provided...
      check        Execute checks and send it to the monitoring server.
      config       Manage configuration packages and stages.
      dump-config  Dump the configuration of the pretiac client.
      events       Subscribe to an event stream.
      objects      Manage configuration objects.
      status       Retrieve status information and statistics for Icinga 2.
      types        Retrieve the configuration object types.
      variables    Request information about global variables.

``pretiac actions``
^^^^^^^^^^^^^^^^^^^

:: 

    Usage: pretiac actions [OPTIONS] COMMAND [ARGS]...

      There are several actions available for Icinga 2 provided by the
      ``/v1/actions`` URL endpoint.

    Options:
      --help  Show this message and exit.

    Commands:
      send-service-check-result  Send a check result for a service and create...

``pretiac actions send-service-check-result``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:: 

    Usage: pretiac actions send-service-check-result [OPTIONS] SERVICE

      Send a check result for a service and create the host or the service if
      necessary.

    Options:
      --plugin-output TEXT     The plugin main output. Does **not** contain the
                               performance data.
      --performance-data TEXT  The performance data.
      --exit-status TEXT       For services: ``0=OK``, ``1=WARNING``,
                               ``2=CRITICAL``, ``3=UNKNOWN``, for hosts: ``0=UP``,
                               ``1=DOWN``.
      --host TEXT              The name of the host.
      --help                   Show this message and exit.

``pretiac config``
^^^^^^^^^^^^^^^^^^

:: 

    Usage: pretiac config [OPTIONS] COMMAND [ARGS]...

      Manage configuration packages and stages.

      Manage configuration packages and stages based on configuration files and
      directory trees.

    Options:
      --help  Show this message and exit.

    Commands:
      delete  Delete a configuration package or a configuration stage entirely.
      show

``pretiac config delete``
^^^^^^^^^^^^^^^^^^^^^^^^^

:: 

    Usage: pretiac config delete [OPTIONS] PACKAGE [STAGE]

      Delete a configuration package or a configuration stage entirely.

    Options:
      --help  Show this message and exit.

``pretiac objects``
^^^^^^^^^^^^^^^^^^^

:: 

    Usage: pretiac objects [OPTIONS] COMMAND [ARGS]...

      Manage configuration objects.

    Options:
      --help  Show this message and exit.

    Commands:
      delete-service  Delete a service.
      list            List the different configuration object types.

``pretiac objects delete-service``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:: 

    Usage: pretiac objects delete-service [OPTIONS] HOST SERVICE

      Delete a service.

    Options:
      --help  Show this message and exit.

``pretiac objects list``
^^^^^^^^^^^^^^^^^^^^^^^^

:: 

    Usage: pretiac objects list [OPTIONS] OBJECT_TYPE

      List the different configuration object types.

    Options:
      --help  Show this message and exit.


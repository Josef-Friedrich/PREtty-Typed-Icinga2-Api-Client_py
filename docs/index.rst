Welcome to pretiac's documentation!
===================================

``pretiac`` stands for **PRE** tty **T** yped **I** cinga2 **A** pi **C** lient.
This project is a fork / extension of the
`TeraIT-at/icinga2apic <https://github.com/TeraIT-at/icinga2apic>`__ api client.
The client class of ``icinga2apic`` was renamed to :class:`pretiac.raw_client.RawClient`.
``pretaic`` provides an additional client (:class:`pretiac.client.Client`), which is typed.
`Pydantic <https://github.com/pydantic/pydantic>`__ is used to validate the
Icinga2 REST API and to convert the JSON
output into Python data types.

.. autofunction:: pretiac.get_default_client
   :no-index:

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

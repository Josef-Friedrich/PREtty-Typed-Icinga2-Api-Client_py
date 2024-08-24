

## <a id="objects-list"></a> objects.list()

To get a list of objects (`Host`, `Service`, ...) use the funtion `objects.list()`. You can use `filters` to ...

  Parameter     | Type       | Description
  --------------|------------|--------------
  object\_type  | string     | **Required.** The object type to get, e.g. `Host`, `Service`.
  name          | string     | **Optional.** The objects name.
  attrs         | list       | **Optional.** Get only the specified objects attributes.
  filters       | string     | **Optional.** The filter expression, see [documentation](http://docs.icinga.org/icinga2/latest/doc/module/icinga2/chapter/icinga2-api#icinga2-api-filters).
  filter\_vars  | dictionary | **Optional.** Variables which are available to your filter expression.
  joins         | bool       | **Optional.** Also get the joined object, e.g. for a `Service` the `Host` object.



## <a id="objects-create"></a> objects.create()

Create an object using `templates` and specify attributes (`attrs`).

  Parameter     | Type       | Description
  --------------|------------|--------------
  object\_type  | string     | **Required.** The object type to get, e.g. `Host`, `Service`.
  name          | string     | **Optional.** The objects name.
  templates     | list       | **Optional.** A list of templates to import.
  attrs         | dictionary | **Optional.** The objects attributes.

Examples:

Create a host:

    client.objects.create(
        'Host',
        'localhost',
        ['generic-host'],
        {'address': '127.0.0.1'})

Create a service for Host "localhost":

    client.objects.create(
        'Service',
        'localhost!dummy',
        ['generic-service'],
        {'check_command': 'dummy'})


## <a id="objects-update"></a> objects.update()

Update an object with the specified attributes.

  Parameter     | Type       | Description
  --------------|------------|--------------
  object\_type  | string     | **Required.** The object type to get, e.g. `Host`, `Service`.
  name          | string     | **Optional.** The objects name.
  attrs         | dictionary | **Optional.** The objects attributes.

Examples:

Change the ip address of a host:

    client.objects.update(
        'Host',
        'localhost',
        {'address': '127.0.1.1'})

Update a service and change the check interval:

    client.objects.create('Service',
           'localhost!dummy',
           ['generic-service'],
           {'check_interval': '10m'})


## <a id="objects-delete"></a> objects.delete()

Update an object with the specified attributes.

  Parameter     | Type       | Description
  --------------|------------|--------------
  object\_type  | string     | **Required.** The object type to get, e.g. `Host`, `Service`.
  name          | string     | **Optional.** The objects name.
  filters       | string     | **Optional.** Filter expression for matching the objects.
  filter\_vars  | dictionary | **Optional.** Variables which are available to your filter expression.
  cascade       | boolean    | **Optional.** Also delete dependent objects. Defaults to `True`.

Examples:

Delete the "localhost":

    client.objects.delete('Host', 'localhost')

Delete all services matching `vhost\*`:

    client.objects.delete('Service', filters='match("vhost\*", service.name)')

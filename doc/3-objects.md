

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


  Parameter     | Type       | Description
  --------------|------------|--------------
  object\_type  | string     | **Required.** The object type to get, e.g. `Host`, `Service`.
  name          | string     | **Optional.** The objects name.
  templates     | list       | **Optional.** A list of templates to import.
  attrs         | dictionary | **Optional.** The objects attributes.




## <a id="objects-update"></a> objects.update()



  Parameter     | Type       | Description
  --------------|------------|--------------
  object\_type  | string     | **Required.** The object type to get, e.g. `Host`, `Service`.
  name          | string     | **Optional.** The objects name.
  attrs         | dictionary | **Optional.** The objects attributes.


## <a id="objects-delete"></a> objects.delete()

Update an object with the specified attributes.

  Parameter     | Type       | Description
  --------------|------------|--------------
  object\_type  | string     | **Required.** The object type to get, e.g. `Host`, `Service`.
  name          | string     | **Optional.** The objects name.
  filters       | string     | **Optional.** Filter expression for matching the objects.
  filter\_vars  | dictionary | **Optional.** Variables which are available to your filter expression.
  cascade       | boolean    | **Optional.** Also delete dependent objects. Defaults to `True`.

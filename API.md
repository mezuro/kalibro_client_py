# API

Describes the general workings of the API, including differences between the Ruby and Python versions.

## Differences to Ruby

* There is no `persisted` attribute
* There is no logger specification
* There is no `create` method, just instantiate the class and call `save`
* Save does not return True or False. In case it fails it raises an exception
* Destroy is called Delete and returns no value. In case it fails it raises an exception

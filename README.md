# KalibroClient

[![Build Status](https://travis-ci.org/mezuro/kalibro_client_py.png?branch=master)](https://travis-ci.org/mezuro/kalibro_client_py)
[![Code Climate](https://codeclimate.com/github/mezuro/kalibro_client_py.png)](https://codeclimate.com/github/mezuro/kalibro_client_py)
[![Coverage Status](https://coveralls.io/repos/mezuro/kalibro_client_py/badge.svg?branch=master&service=github)](https://coveralls.io/github/mezuro/kalibro_client_py?branch=master)

KalibroClient is a Python package intended to be an interface for Python 2 applications who want to use the open source code analysis webservice Kalibro (http://github.com/mezuro/kalibro_processor http://github.com/mezuro/kalibro_configurations).

There are some differences to the original Ruby version (http://github.com/mezuro/kalibro_client) of this which you can find at the file `API.md`.

## Installation

ATTENTION: this package has not been released yet. The installation step are not expected to work yet!

Add it to your `requirements.txt` or simply run:

    pip install kalibro_client

## Usage

KalibroClient is intended to be an easy interface that encapsulates the usage of all the Kalibro service's endpoints. So have a look at the available entities at the folders `kalibro_client/processor` and `kalibro_client/configurations`.

All the entities have `Base` mixed in, so have a good look at it. Specially notice that all the entities have methods:

* `save`
* `exists?`
* `find`
* `destroy`

These four methods should be useful.

We hope to make available soon a full documentation that will make easier to understand all this.

## Contributing

0. Install virtualenv (https://virtualenv.pypa.io/en/latest/)
1. Fork this repository
2. Create a virtualenv inside the fork clone (`virtualenv ENV`)
3. Activate the environment (`source ENV/bin/activate`)
4. Install the reuirements (`pip install -r requirements.txt`)
5. Make your modifications and changes
6. Commit your changes (`git commit -am 'Add some feature'`)
7. Push to the branch (`git push -u origin my-new-feature`)
8. Create a new Pull Request

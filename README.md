## Biblica Bot

![status: active](https://img.shields.io/badge/status-active-green.svg)

This Telegram bot hopes to make the Bible more accessible, and hopefully to give a timely answer to those looking for it. 

### Installing Libraries
Add new libraries either in app.yaml or add them to requirements.txt (Note that adding them to requirements.txt won't automatically import the libraries! You need to pip install them into a \lib folder still)

### Feedback
Star this repo if you found it useful. Use the github issue tracker to give
feedback on this repo.

## Licensing
See [LICENSE](LICENSE)

## Author
Hi, I'm [Julwrites](http://www.tehj.org)

## Code Guidelines

### Modules
This framework aims to implement a lightweight and reusable set of modules. 

Nested modules are allowed, although not preferred, and the depth of nesting should be kept minimal. 

Module names fall into 3 core blocks, each prefixed by the module name.
e.g. module admin contains admin_utils, admin_actions, admin_hooks. 
This facilitates a simple naming scheme, and even code generation. 

### Code
We are using Python27 for this version of the framework.

Naming Convention:
* Variables should be named using underscore_case.
* Methods should be named using camelCase.
* Classes should be named using PascalCase.
* Modules should be named using underscore_case, in keeping with Python STL.

This keeps the entities visually separate, and syntax clean.

As much as possible, each file should contain one of 3 things:
* A class and related methods
* A set of utility methods
* Business logic/End point logic

This is intended to facilitate separation of responsibility for loose coupling. 

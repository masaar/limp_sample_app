# LIMP Sample App
You can use this app as quick reference of how to build apps for LIMP backend.

# Packages
This repo represents a package. A package is a folder with number of python files containing LIMP modules. The package is having a distinguishing `__init__.py` file (which is also a requirement of Python packages) that sets the configurations of a package. An app in the LIMP eco-system could be the results of multiple packages that's one reason to allow LIMP structure to have more than a single package with the ability to manage them using LIMP CLI interface.

# Modules
A LIMP module is a single class in a Python file inside a LIMP package inheriting LIMP built-in `BaseModule` class. The `BaseModule` singletones all LIMP modules and provides them with access to the unified internal API for exchanging data.
A module is essentially a definition of a data-type with number of typed-`attrs` that can be set as `optional_attrs` and/or auto-extended by documents from the same and/or another module using the `extns` instructions. A module as well defines all its `methods` that any client could call. By default the `CRUD` methods, `read`, `create`, `update`, `delete` are available for all of the modules by simply defining them. Additional methods can be defined either for use by the `GET` interface, or more usual `websocket` interface using some additional instructions passed. A method can set the permissions checks required for an agent to pass before the agent being allowed to access the called method.

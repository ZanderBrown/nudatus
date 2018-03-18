Nudatus
=======

Nudatus is a tool to remove comments from python scripts

It's created for use in uflash_ to help squeeze longer programs onto the micro:bit but it should be suitable for various environments with restricted storage

*Note* Nudatus uses the tokenizer built into Python so only supports the syntax of the version it's running on but it's extreamly unlikly this will cause you any issues (print is handled fine)

Usage
--------

Nudatus is designed to be embedded within a greater tool (like uflash_ or Mu_ by ntoll_) but also provides a CLI tool


.. code:: text

    nudatus [-h] [--version] [input] [output]


An input file must be specified but if output is omitted the result will be printed on stdout

Calling from a Python script is quite simple:

.. code:: python

    import nudatus
    source = '' # Input script
    result = nudatus.mangle(source) # Result as str

.. _uflash: https://github.com/ntoll/uflash
.. _Mu: http://codewith.mu/
.. _ntoll: http://ntoll.org/

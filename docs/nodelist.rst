Nodelist
========

If a ``--nodelist`` is passed, it will be used to count online Nodes and
Clients from there.
It can either be a local file, or if this does not exist,
it is interpreted as URL, and fetched from there.

If successful, the numbers will be added to the APIfile::

    {
      "state": {
        "nodes": 0,
        "description": ""
      }
    }

Would be changed to this::

    {
      "state": {
        "nodes": 23,
        "description": "[23 Nodes, 42 Clients]"
      }
    }


.. automodule:: ffflash.inc.nodelist
    :members:
    :undoc-members:
    :private-members:


Rankfile
--------

.. automodule:: ffflash.inc.rankfile
    :members:
    :undoc-members:
    :private-members:

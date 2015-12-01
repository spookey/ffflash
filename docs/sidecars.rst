Sidecars
========

Use one ore more Sidecars to merge content from there into the APIfile.

Sidecars are either *yaml* or *json* files.
This is determined by the extension in the filename.

The filename is a dot-separated path into the keys of the APIfile.
If that path does not exist in the APIfile, it will be ignored.

Only if a Sidecar itself does not exist yet or is empty,
it will be generated with the contents read from the APIfile.

Assuming this APIfile::

    {
      "support": {
        "club": {
          "name": "Supporter Club",
          "city": "Generic City",
          "street": "Some Street 23",
          "zip": "23425"
        },
        "donations": {
          "bankaccount": {
            "BIC": "ABC123DEFXX",
            "IBAN": "GC13370000000123456789",
            "usage": "I like cash"
          }
        }
      }
    }

Valid filenames and their content would be these:

* ``/path/to/your/sidecars/support.club.city.yaml``::

    Generic City
    ...


* ``/path/to/your/sidecars/support.club.yaml``::

    city: Generic City
    name: Supporter Club
    street: Some Street 23
    zip: '23425'


* ``/path/to/your/sidecars/support.yaml``::

    club:
        city: Generic City
        name: Supporter Club
        street: Some Street 23
        zip: '23425'
    donations:
        bankaccount:
            BIC: ABC123DEFXX
            IBAN: GC13370000000123456789
            usage: I like cash


* ``/path/to/your/sidecars/support.donations.bankaccount.usage.json``::

    "I like cash"

* ``/path/to/your/sidecars/support.donations.bankaccount.json``::

    {
      "BIC": "ABC123DEFXX",
      "IBAN": "GC13370000000123456789",
      "usage": "I like cash"
    }

* ``/path/to/your/sidecars/support.donations.json``::

    {
      "bankaccount": {
        "BIC": "ABC123DEFXX",
        "IBAN": "GC13370000000123456789",
        "usage": "I like cash"
      }
    }

Invalid filenames would be these:

* ``/path/to/your/sidecars/support.club.city.txt``:

    Wrong extension

* ``/path/to/your/sidecars/support.industry.json``:

    Key *industry* is not present in APIfile.

* ``/path/to/your/sidecars/support.donations.bankaccount.iban.yaml``:

    *iban* can't be found, it's case sensitive. Use *IBAN* instead.


Duplicated Sidecar content is handled like this.
Assuming these Sidecars with this content:

* ``support.club.street.yaml``::

    Same Street 5
    ...

* ``support.club.yaml``::

    city: Generic City
    name: Supporter Club
    street: Another Street 42
    zip: '23425'

The List of Sidecars is sorted, so the longer filename is handled first.
So the shorter filename wins, the result is then::

    {
      "support": {
        "club": {
          "name": "Supporter Club",
          "city": "Generic City",
          "street": "Another Street 42",
          "zip": "23425"
        }
    }


.. automodule:: ffflash.inc.sidecars
    :members:
    :undoc-members:
    :private-members:

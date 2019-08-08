=====
qngng
=====

**qngng**, the Queb name generator: *next generation*.

This is a fork of the more basic `qng <https://github.com/abusque/qng>`_
project which includes the novel ``qngng-uda`` program to generate a
random name from the `UDA <https://uda.ca/>`_ directory.

Unfortunately, the qng maintainer is unresponsive and won't follow up
with community contributions, so this fork is necessary.


Requirements
------------
To run **qngng**, you only need Python ≥ 3.6.


Installing
----------
To install **qngng** system-wide, run:

.. code-block:: sh

   $ sudo pip3 install qngng

To install **qngng** manually from source, the steps are as follows:

.. code-block:: sh

   $ git clone https://github.com/eepp/qngng
   $ cd qngng
   $ sudo ./setup.py install


Usage
-----
qngng
~~~~~
Once installed, you can use **qngng**:

.. code-block:: sh

   $ qngng

This generates a single random Queb name.

You can also generate names for a specific gender:

.. code-block:: sh

   $ qngng --gender=male

Generate names according to their relative popularity:

.. code-block:: sh

   $ qngng --weighted

Generate a name formatted as "snake_case" without any diacritics:

.. code-block:: sh

   $ qngng --snake-case

Generate a name formatted as "kebab-case" without any diacritics:

.. code-block:: sh

   $ qngng --kebab-case

qngng-uda
~~~~~~~~~
If you want to get a real `UDA <https://uda.ca/>`_ member name, you can
use ``qngng-uda``:

.. code-block:: sh

   $ qngng-uda

Like ``qngng``, ``qngng-uda`` supports the ``--gender``, ``--snake-case``,
and ``--kebab-case`` options.

You can get the name of an UDA actor, host (*animateur* in French), or
singer with the ``--type`` option:

.. code-block:: sh

   $ qngng-uda --type=actor
   $ qngng-uda --type=host
   $ qngng-uda --type=singer


Sources
-------
The data for **qngng** was sourced from l'`Institut de la statistique
<http://www.stat.gouv.qc.ca/statistiques/population-demographie/caracteristiques/noms_famille_1000.htm>`_
for surnames, and from `PrénomsQuébec.ca
<https://www.prenomsquebec.ca/>`_ for first names (who in turn get their
data from Retraite Québec's `Banque de prénoms
<https://www.rrq.gouv.qc.ca/fr/enfants/banque_prenoms/Pages/banque_prenoms.aspx>`_).

The data for the ``qngng-uda`` command was sourced from the April 2019
UDA directory.

Scripts used for scraping the data from the web pages are in the
``scripts`` directory.

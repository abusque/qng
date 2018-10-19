===
qng
===

.. image:: https://img.shields.io/pypi/v/qng.svg
   :target: https://pypi.org/project/qng/
   :alt: PyPI

*Documentation also available in* `English <README.rst>`_

**qng**, le générateur de noms Queb.

Pré-requis
----------

Pour utiliser **qng**, vous aurez uniquement besoin de Python ≥ 3.4.

Pour l'installation, nous recommandons l'utilisation du gestionnaire
de paquets ``pip``.

Installation
------------

Pour installer **qng** sur l'ensemble du système, exécutez:

.. code-block:: sh

   sudo pip3 install qng

Pour installer **qng** manuellement à partir du code source, les
étapes sont les suivantes:

.. code-block:: sh

   git clone git@github.com:abusque/qng.git
   cd qng
   sudo ./setup.py install

Utilisation
-----------

Une fois installé, vous pouvez utiliser **qng** avec la commande
suivante:

.. code-block:: sh

   qng

Cette commande génère un seul nom Queb aléatoire.

Vous pouvez aussi générer un nom d'un genre donné:

.. code-block:: sh

   qng --gender male

Générer seulement une partie d'un nom:

.. code-block:: sh

   qng --part first

Générer un nom relativement à sa popularité:

.. code-block:: sh

   qng --weighted


Générer un nom formaté en «snake_case», sans diacritiques (pratiquer
pour nommer des «containers»):

.. code-block:: sh

   qng --snake-case

Voici comment l'appliquer pour nommer un container Docker:

.. code-block:: sh

   docker run --name $(qng --snake-case) hello-world

Pour automatiquement générer un nom Queb pour vos containers Docker,
vous pouvez aussi utiliser
`dockeb <https://github.com/abusque/dockeb>`_.

Toutes les options précédentes peuvent être combinées si
voulu. Référez-vous à la commande d'aide pour plus de détails:

.. code-block:: sh

   qng --help

API Python
^^^^^^^^^^

Vous pouvez aussi utiliser **qng** via son API Python, pour l'intégrer
avec d'autres applications,

Voici un exemple simple de son utilisation programmatique:

.. code-block:: python

   import qng.generator

   generator = qng.generator.QuebNameGenerator()
   name = generator.generate()
   print(name)

La fonction ``generate()`` supporte aussi les options suivantes, avec
la même signification que les options correspondantes dans l'outil en
ligne de commande:

.. code-block:: python

   import qng.generator

   generator = qng.generator.QuebNameGenerator()
   name = generator.generate(
       gender='male',
       part='first',
       snake_case=True,
       weighted=True,
   )
   print(name)

Référez-vous à la documentation dans le code source pour plus de
détails.

Développement
-------------

Pour développer **qng** localement, vous pouvez utiliser `pipenv
<https://docs.pipenv.org/>`_. Exécutez ``pipenv install --dev`` pour
générer un environnement virtuel (*virtual environment*) dans lequel
les dépendances seront installées. Vous pouvez ensuite utiliser
``pipenv shell`` pour activer cet environnement.

Pour publier de nouvelles versions sur PyPI, nous recommandons
l'utilisation de `Twine <https://pypi.org/project/twine/>`_.

Références
----------

Les données pour **qng** proviennent de `l'institut de la
statistique`_ pour les noms de famille, ainsi que de
`PrénomsQuébec.ca`_ pour les prénoms (eux-mêmes ayant tiré leurs
données de la `banque de prénoms`_ de Retraite Québec).

Les scripts utilisés pour extraire les données des pages web peuvent
être trouvés dans le répertoire ``scripts/``.

.. _l'institut de la statistique: http://www.stat.gouv.qc.ca/statistiques/population-demographie/caracteristiques/noms_famille_1000.htm
.. _PrénomsQuébec.ca: https://www.prenomsquebec.ca/
.. _banque de prénoms: https://www.rrq.gouv.qc.ca/fr/enfants/banque_prenoms/Pages/banque_prenoms.aspx

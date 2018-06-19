# qng

**qng**, the Queb name generator.

## Requirements

To run **qng**, you will only need Python ≥ 3.6.

For installing, we recommend using the `pip` package manager.

## Installing

To install **qng** system-wide, run:

```sh
sudo pip3 install qng
```

To install **qng** manually from source, the steps are as follows:

```sh
git clone git@github.com:abusque/qng.git
cd qng
sudo ./setup.py install
```

## Using

Once installed, you can use **qng** by running the following command:

```sh
qng
```

This will generate a single random Queb name.

You can also generate names for a specific gender:

```sh
qng --gender male
```

Generate names according to their relative popularity:

```sh
qng --weighted
```

Generate a name formatted as "snake_case" without any diacritics
(useful for naming your containers):

```sh
qng --snake-case
```

All the above options may be combined if desired. Refer to the help
for more details:

```sh
qng --help
```

## Development

For local development of **qng**, you may use
[pipenv](https://docs.pipenv.org/). Use `pipenv install --dev` to
generate a virtual environment into which the dependencies will be
installed. You may then use `pipenv shell` to activate that
environment.

For publishing releases to PyPI, we recommend using
[Twine](https://pypi.org/project/twine/).

## References

The data for **qng** was sourced from [l'institut de la
statistique][stats qc] for surnames, and from
[PrénomsQuébec.ca][prenoms qc] for first names (who in turn get their
data from Retraite Québec's [banque de prénoms][prenoms rrq]).

Scripts used for scraping the data from the web pages can be found
under the `scripts/` directory.

[stats qc]: http://www.stat.gouv.qc.ca/statistiques/population-demographie/caracteristiques/noms_famille_1000.htm
[prenoms qc]: https://www.prenomsquebec.ca/
[prenoms rrq]: https://www.rrq.gouv.qc.ca/fr/enfants/banque_prenoms/Pages/banque_prenoms.aspx

# 22q11-ibbc-genomic-db

22q11-ibbc-genomic-db is a Django powered webapp for the International 22q11.2 Consortium on Brain and Behavior Consortium.
The International Consortium on Brain and Behavior in 22q11.2 Deletion Syndrome (22q11DS) is a collaborative RO1 of 22 institutions,
with one genomic and four phenotyping leading sites. The collaboration combines genomic with neuropsychiatric and neurobehavioral
paradigms to advance the understanding of the pathogenesis of schizophrenia (SZ) and related phenotypes. The Consortium provides
the largest available sample to date of 1000 genetically and phenotypically characterized individuals with 22q11DS.

webapp: [www.22q11-ibbc.org](http://22q11-ibbc.org)

# Requirements

- Django: * See requirements.txt
- nginx
- gunicorn

# Installation

Download packages

	git clone https://github.com/drhee/22q11-ibbc-genomic-db.git

Install pip packages using requirements

	pip install -r requirements.txt

Export an environment key in .bashrc
	
	export SECRET_KEY = 'something'

Modify the following

	settings/*
	templates/data/data_documents_*

Collect all static - ensure nginx's static points to assets

	python manage.py collectstatic --settings=22q11-ibbc.settings.local

Change site name
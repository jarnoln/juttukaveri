# Juttukaveri

Speech interface to ChatGPT

Created using:
* [Django](https://www.djangoproject.com/)(4.2)
* [Django REST framework](https://www.django-rest-framework.org/)
* Speech-to-Text: OpenAI Whisper
* Text-to-Speech: Amazon Polly

Install
-------

Get sources:

    git clone https://github.com/jarnoln/juttukaveri.git

Create virtual environment and install Python packages:

    mkvirtualenv -p /usr/bin/python3 juttukaveri
    pip install -r requirements.txt

Generate site configuration:

    python juttukaveri/generate_site_config.py juttukaveri/site_config.py

Initialize DB:

    python manage.py migrate

Run development server:

    python manage.py runserver



Deploy
------

[Install Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)

    pip install -r requirements-deploy.txt

Edit `ansible/inventory.example`  with your actual host information and rename it to `ansible/inventory`. Then:

    ansible-playbook -i ansible/inventory ansible/provision-deb.yaml
    invoke deploy --user=[your_username] --host=[your_host]

This will create `atange/site_config.py`-file with default values, but they need to be replaced with
actual host-specific values (especially `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS`)

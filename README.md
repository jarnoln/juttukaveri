# Juttukaveri

Voice interface to ChatGPT

Idea to this came when my daughter was attempting to have conversation with car navigator voice.

"Hmm, wouldn't it be nice if it could actually listen to her and respond?"

She could have conversation with ChatGPT if only she could read and write, but it will probably still be a few years
before she can master those. But since there are tools to convert speech to text and text to speech, it should be
possible to  create a voice interface to ChatGPT which can be used without knowing how to read or write. And it was.

This might be useful also when she starts asking difficult questions that I would need to google for answers. Now I
can just tell her to ask the nice AI lady and save myself the trouble. Or if she asks for a bedtime story. Or just
feels bored and wants to talk with somebody. A small step towards delegating all kinds to parenting responsibilities to
AI.

Created using:
* [Django](https://www.djangoproject.com/)(4.2)
* [Django REST framework](https://www.django-rest-framework.org/)
* Speech-to-Text: [OpenAI Whisper](https://platform.openai.com/docs/guides/speech-to-text)
* Response generation: [OpenAI ChatGPT](https://platform.openai.com/docs/guides/gpt/chat-completions-api)
* Text-to-Speech: [Amazon Polly](https://aws.amazon.com/polly/)

Operation:
1. Record speech
2. Send recording to OpenAI Whisper which converts it to text
3. Send text to ChatGPT and receive a response
4. Send response text to Amazon Polly to convert it to speech audio file
5. Play back audio file
6. Rinse and repeat


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

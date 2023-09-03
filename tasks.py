import os

from invoke import task
from fabric import Connection


REPO_URL = "git@github.com:jarnoln/juttukaveri.git"


@task
def deploy(context, user, host):
    print("Deploying to {}@{}".format(user, host))
    site_name = host
    site_folder = "/home/{}/sites/{}".format(user, site_name)
    source_folder = os.path.join(site_folder, "source")
    virtualenv = os.path.join(site_folder, "virtualenv")
    python = virtualenv + "/bin/python"
    pip = virtualenv + "/bin/pip"
    django_setting_directory_name = "juttukaveri"
    app_name = "juttukaveri"
    connection = Connection(host=host, user=user)
    _create_directory_structure_if_necessary(connection, site_folder)
    _init_virtualenv(connection, site_folder)
    _get_latest_source(connection, source_folder)
    _install_virtualenv_libraries(connection, source_folder, pip)
    # _run_pipenv(connection, source_folder, virtualenv, python)
    _check_site_config(connection, source_folder, django_setting_directory_name, python)
    _update_database(connection, source_folder, python)
    # _update_static_files(connection, source_folder)
    _run_remote_unit_tests(
        connection, source_folder, django_setting_directory_name, python
    )
    _check_settings(connection, source_folder, django_setting_directory_name, python)
    _restart_gunicorn(connection, app_name)
    _restart_nginx(connection)


def _create_directory_structure_if_necessary(c, site_folder):
    c.run("mkdir -p %s" % site_folder)
    for sub_folder in ("database", "log", "static", "db"):
        c.run("mkdir -p %s/%s" % (site_folder, sub_folder))
    c.run("sudo mkdir -p /var/log/gunicorn")


def _init_virtualenv(c, site_folder):
    virtualenv_path = site_folder + "/virtualenv"
    # if not exists(site_folder + '/virtualenv'):
    if c.run("test -d {}".format(virtualenv_path), warn=True).failed:
        c.run("cd {} && virtualenv --python=python3 virtualenv".format(site_folder))


def _get_latest_source(c, source_folder):
    git_folder = "{}/.git".format(source_folder)
    if c.run("test -d {}".format(git_folder), warn=True).failed:
        c.run("git clone {} {}".format(REPO_URL, source_folder))
        # Note: This may fail until cloned once manually
        c.run("cd {} && git config pull.rebase false".format(source_folder))
    else:
        c.run("cd {} && git pull".format(source_folder))


def _run_pipenv(c, source_folder, virtualenv, python):
    """Not yet in use, Pipenv does not currently work properly"""
    c.run(
        "cd {} && VIRTUAL_ENV={} pipenv --python={} install --deploy".format(
            source_folder, virtualenv, python
        )
    )


def _install_virtualenv_libraries(c, source_folder, pip):
    # TODO: Check Python version. For now assume version 3.9.
    c.run("cd {} && {} install -r requirements.txt".format(source_folder, pip))
    c.run("cd {} && {} install -r requirements-server.txt".format(source_folder, pip))


def _check_site_config(c, source_folder, django_setting_directory_name, python):
    settings_folder = os.path.join(source_folder, django_setting_directory_name)
    site_config_file = os.path.join(settings_folder, "site_config.py")
    if c.run("test -f {}".format(site_config_file), warn=True).failed:
        c.run(
            "{} {}/generate_site_config.py {}".format(
                python, settings_folder, site_config_file
            )
        )


def _update_database(c, source_folder, python):
    c.run("cd {} && {} manage.py makemigrations".format(source_folder, python))
    c.run("cd {} && {} manage.py migrate".format(source_folder, python))


def _update_static_files(c, source_folder):
    c.run(
        "cd {} && ../virtualenv/bin/python manage.py collectstatic --noinput".format(
            source_folder
        )
    )


def _run_remote_unit_tests(c, source_folder, django_settings_directory_name, python):
    print("*** Run remote unit tests")
    c.run(
        "cd {} && {} manage.py test --settings={}.settings".format(
            source_folder, python, django_settings_directory_name
        )
    )


def _check_settings(c, source_folder, django_settings_directory_name, python):
    print("*** Run remote unit tests")
    c.run(
        "cd {} && {} manage.py check --deploy --settings={}.settings".format(
            source_folder, python, django_settings_directory_name
        )
    )


def _restart_gunicorn(c, app_name):
    c.run("sudo systemctl restart {}.gunicorn".format(app_name))


def _restart_nginx(c):
    c.run("sudo service nginx restart")

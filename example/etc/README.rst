etc
===

Sample Web Server configuration files:

- nginx.conf
- supervisor.conf

Sample deployment layout::

    /home/frontend-forms/
    ├── django-frontend-forms
    ├── etc
    ├── logs
    ├── python
    ├── run
    ├── setenv.bash
    └── sservicesctl.py

Usage:

.. code:: bash

    cp -R /home/frontend-forms/django-frontend-forms/example/etc /home/frontend-forms/
    ... adjust files if as required ...
    sudo ln -s /home/frontend-forms/etc/nginx.conf /etc/nginx/sites-enabled/frontend-forms.conf
    sudo ln -s /home/frontend-forms/etc/supervisor.conf /etc/supervisor/conf.d/frontend-forms.conf

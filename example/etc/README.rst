etc
===

Sample Web Server configuration files:

- nginx.conf
- supervisor.conf

Sample deployment layout::

    /home/django-frontend-forms-demo/
    ├── django-frontend-forms
    ├── etc
    ├── logs
    ├── python
    ├── run
    ├── setenv.bash
    └── sservicesctl.py

Usage:

.. code:: bash

    cp -R /home/django-frontend-forms-demo/django-frontend-forms/example/etc /home/django-frontend-forms-demo/
    ... adjust files if as required ...
    sudo ln -s /home/django-frontend-forms-demo/etc/nginx.conf /etc/nginx/sites-enabled/django-frontend-forms-demo.conf
    sudo ln -s /home/django-frontend-forms-demo/etc/supervisor.conf /etc/supervisor/conf.d/django-frontend-forms-demo.conf

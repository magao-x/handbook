SSL Certificates
================

To get updated SSL certificates for the instrument machines, use the LEGO tool as ``xsup``.

Brand-new certificates
----------------------

1. ``xsupify``
2. ``export VULTR_API_KEY=``...  (Using `Vultr API <https://go-acme.github.io/lego/dns/vultr/>`_ as an example)
3. ``lego --email lynx@magao-x.org --dns vultr --domains exao1.magao-x.org --domains exao2.magao-x.org --domains exao3.magao-x.org run`` (answering ``Y`` if prompted to accept terms)
4. New certificates will now be in ``/home/xsup/.lego`` on AOC.

Renew certificates
------------------

5. ``lego --email lynx@magao-x.org --dns vultr --domains exao1.magao-x.org --domains exao2.magao-x.org --domains exao3.magao-x.org renew``

.. _sup_certs:

Installing certificates for sup
-------------------------------

The ``sup`` web UI has certificates configured as part of its SystemD unit::

    root@exao1:~# cat /etc/systemd/system/sup.service.d/override.conf
    [Service]
    Environment="UVICORN_HOST=0.0.0.0"
    Environment="UVICORN_PORT=4433"
    Environment="MAGAOX_ROLE=AOC"
    Environment="UVICORN_SSL_KEYFILE=/home/xsup/.lego/certificates/exao1.magao-x.org.key"
    Environment="UVICORN_SSL_CERTFILE=/home/xsup/.lego/certificates/exao1.magao-x.org.crt"
    Environment="UVICORN_CA_CERTS=/home/xsup/.lego/certificates/exao1.magao-x.org.issuer.crt"


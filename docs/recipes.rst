=======
Recipes
=======

.. note::
    You'll need to create an API key to be able to use these recipes. See the
    :doc:`getting_started` page to begin. The following examples assume the API
    keys are set using environment variables, but they can be provided as
    arguments to the :class:`~hostedpi.picloud.PiCloud` class constructor.

Provisioning Pis
================

Provision a Pi
--------------

.. code-block:: python

    from hostedpi import PiCloud

    cloud = PiCloud()

    pi = cloud.create_pi('', model=3, disk=10)

Provision some Pis
------------------

.. code-block:: python

    from hostedpi import PiCloud

    cloud = PiCloud()

    pis = [
        cloud.create_pi('mypi{}'.format(n), model=3, disk=10)
        for n in range(10)
    ]

Push button to provision a Pi
-----------------------------

.. code-block:: python

    from hostedpi import PiCloud
    from gpiozero import Button, LED

    cloud = PiCloud()
    btn = Button(2)
    led = LED(3)

    def make_pi():
        name = "helloworld"
        cloud.create_pi(name)
        led.on()

    btn.when_pressed = make_pi

See a live demo at https://twitter.com/ben_nuttall/status/1300442981779025921

.. note::
    This requires the `gpiozero`_ library.

.. _gpiozero: https://gpiozero.readthedocs.io/

Retrieving data about Pis
=========================

List all Pis
------------

.. code-block:: python

    from hostedpi import PiCloud

    cloud = PiCloud()

    for name in cloud.pis:
        print(name)

List all Pis and their IPv6 address
-----------------------------------

.. code-block:: python

    from hostedpi import PiCloud

    cloud = PiCloud()

    for name, pi in cloud.pis.items():
        print(name, pi.ip)

Rebooting
=========

Reboot all Pis
--------------

.. code-block:: python

    from hostedpi import PiCloud

    cloud = PiCloud()

    for pi in cloud.pis.values():
        pi.reboot()

Reboot all Pis powered off
--------------------------

.. code-block:: python

    from hostedpi import PiCloud

    cloud = PiCloud()

    for pi in cloud.pis.values():
        if not pi.power:
            pi.reboot()

Reboot all Pis not responding to ping
-------------------------------------

.. note::
    :meth:`~hostedpi.pi.Pi.ping_ipv6` requires an IPv6 internet connection, and no IPv4 equivalent is
    available

.. code-block:: python

    from hostedpi import PiCloud

    cloud = PiCloud()

    for pi in cloud.pis.values():
        if not pi.ping_ipv6():
            pi.reboot()

SSH
===

List SSH commands for all Pis
-----------------------------

.. code-block:: python

    from hostedpi import PiCloud

    cloud = PiCloud()

    for pi in cloud.pis.values():
        print(pi.ssh_command)

Write SSH config to a file
--------------------------

.. code-block:: python

    from hostedpi import PiCloud

    cloud = PiCloud()

    with open('config', 'w') as f:
        f.write(cloud.ssh_config)

Ping
====

.. note::
    :meth:`~hostedpi.pi.Pi.ping_ipv6` requires an IPv6 internet connection, and
    no IPv4 equivalent is available

Ping all Pis every minute
-------------------------

List style:

.. code-block:: python

    from hostedpi import PiCloud
    from time import sleep

    cloud = PiCloud()
    pi = cloud.pis['somepi']

    while True:
        for name, pi in cloud.pis.items():
            if pi.ping_ipv6():
                print(name, "is up")
            else:
                print(name, "is down")
            sleep(60)

Unit test style:

.. code-block:: python

    from hostedpi import PiCloud
    from time import sleep

    cloud = PiCloud()
    pi = cloud.pis['somepi']

    while True:
        results = ['.' if pi.ping_ipv6() else 'F' for pi in cloud.pis.values()]
        print(''.join(results))
        sleep(60)

Ping status LED
---------------

.. code-block:: python

    from hostedpi import PiCloud
    from gpiozero import LED
    from time import sleep

    cloud = PiCloud()
    pi = cloud.pis['somepi']
    led = LED(2)

    while True:
        if pi.ping_ipv6():
            led.on()
        else:
            led.off()
        sleep(60)

.. note::
    This requires the `gpiozero`_ library.

.. _gpiozero: https://gpiozero.readthedocs.io/

Web
===

Retrieve the contents of the homepage
-------------------------------------

.. note::
    Note that a web server must be installed on the Pi for the URL to resolve in
    a web browser, and an SSL certificate must be created for the https URL to
    resolve.

Print them out:

.. code-block:: python

    from hostedpi import PiCloud
    import requests

    cloud = PiCloud()
    pi = cloud.pis['somepi']

    print(pi.get_web_contents(ssl=True))

Save to a file:

.. code-block:: python

    from hostedpi import PiCloud
    import requests

    cloud = PiCloud()
    pi = cloud.pis['somepi']

    with open('pi.html', 'w') as f:
        f.write(pi.get_web_contents(ssl=True))

Access a particular web location
--------------------------------

Access ``data.json`` from the web server, and print out the ``message`` value:

.. code-block:: python

    from hostedpi import PiCloud
    import requests

    cloud = PiCloud()
    pi = cloud.pis['somepi']

    url = pi.url_ssl + '/data.json'
    r = requests.get(url)
    data = r.json()
    print(data['message'])

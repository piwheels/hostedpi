===============
Getting started
===============

Create a Mythic Beasts account
==============================

1. Sign up: https://www.mythic-beasts.com/user/login

Create an API key
=================

1. Log in to your Mythic Beasts account: https://www.mythic-beasts.com/user/login

2. Open the API Keys page: https://www.mythic-beasts.com/customer/api-users

3. Enter a descriptive name for your API key, for your own reference

4. Check the *Raspberry Pi Provisioning* box

5. Click the *Create API key* button

6. Make a note of the API ID and Secret. You'll need them to use this Python
module, and you can't retrieve them after this screen is gone.

.. note::
    If you lose your keys, you can simply reset them or create a new API key.

Test your API keys
==================

1. To test your API connection, try running the following commands in a terminal
window, with your API ID and secret:

.. code-block:: console

    $ HOSTEDPI_ID='YOUR ID' HOSTEDPI_SECRET='YOUR SECRET' hostedpi test

If your API ID and secret are correct, you should see the response "Connected
to Mythic Beasts API".

Start using the Python module
=============================

Open a Python shell and 

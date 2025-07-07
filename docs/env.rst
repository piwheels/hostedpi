=====================
Environment variables
=====================

Environment variables are used to configure *hostedpi*. They can be set in your
shell, or in a `.env` file in your project directory.

We use the following environment variables:

+------------------------+-----------------------------------------------------------------+------------+
| Environment variable   | Description                                                     | Default    |
+========================+=================================================================+============+
| ``HOSTEDPI_ID``        | Your API key's ID                                               | (required) |
+------------------------+-----------------------------------------------------------------+------------+
| ``HOSTEDPI_SECRET``    | Your API key's secret                                           | (required) |
+------------------------+-----------------------------------------------------------------+------------+
| ``HOSTEDPI_LOG_LEVEL`` | Level of logging: ``DEBUG``, ``INFO``, ``WARNING`` or ``ERROR`` | ``ERROR``  |
+------------------------+-----------------------------------------------------------------+------------+

See :doc:`getting_started` for more information on how to obtain your API key.

For advanced use only:

+-----------------------+------------------------------------+----------------------------------------+
| Environment variable  | Description                        | Default                                |
+=======================+====================================+========================================+
| ``HOSTEDPI_AUTH_URL`` | URL of the authentication endpoint | https://auth.mythic-beasts.com/login   |
+-----------------------+------------------------------------+----------------------------------------+
| ``HOSTEDPI_API_URL``  | URL of the API endpoint            | https://api.mythic-beasts.com/beta/pi/ |
+-----------------------+------------------------------------+----------------------------------------+
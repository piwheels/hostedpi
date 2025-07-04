=====================================
Available Raspberry Pi Specifications
=====================================

This page lists the available specifications for Raspberry Pi servers that can be provisioned using
the *hostedpi* module.

+--------+--------+-----------+
| Model  | Memory | CPU Speed |
+========+========+===========+
| 3      | 1 GB   | 1.2 GHz   |
+--------+--------+-----------+
| 4      | 4 GB   | 1.5 GHz   |
+--------+--------+-----------+
| 4      | 8 GB   | 1.5 GHz   |
+--------+--------+-----------+
| 4      | 8 GB   | 2.0 GHz   |
+--------+--------+-----------+

See further specification details at https://www.mythic-beasts.com/order/rpi and
https://www.raspberrypi.com/products/

.. note::

    When provisioning a Raspberry Pi 3, it could be a 3B or 3B+. It is not possible to specify which
    specific model, but you can see which model you have provisioned by using
    :command:`hostedpi show --full` or :attr:`~hostedpi.pi.Pi.model_full`.

.. note::

    It may be possible that the requested specification is not available at the time of
    provisioning. If this is the case, the module will raise an error saying it's out of stock.

.. warning::

    If new models or specifications are made available by Mythic Beasts, they will not be able to be
    provisioned using the *hostedpi* module until the module is updated to include them. We will
    endeavour to keep the module up to date with the latest specifications, but there may be a delay
    between new specifications being made available and the module being updated to include them.
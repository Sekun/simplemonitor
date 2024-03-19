gotify - create a message
^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: ../creds-warning.rst

.. confval:: url
   :type: string
   :required: true

   your gotify server instance

.. confval:: token

    :type: string
    :required: true

    the application token required to write a message

.. confval:: timeout

    :type: int
    :required: false
    :default: ``5``

    Timeout for HTTP request to Telegram

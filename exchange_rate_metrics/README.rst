=====================
Exchange Rate Metrics
=====================

Overview
========

Provides metrics for the active exchange rates.

The metrics are served at ``/metrics/exchange_rates``. ``/metrics`` is left to
``monitoring_prometheus``. Requests must send ``Authorization: Bearer <key>``, where
``<key>`` is an API key with the ``metrics`` scope belonging to a user who can read
active currencies. Requests without a valid key get HTTP 401.

The key must have the ``metrics`` scope (created via ``res.users.apikeys._generate``).


Credits
=======

Authors
~~~~~~~

* Ross Golder <ross@golder.org>

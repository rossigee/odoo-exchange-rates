# Copyright 2016-2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from prometheus_client import Gauge, generate_latest

from odoo.http import Controller, route, request

import time

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class ExchangeRateMetrics(metaclass=Singleton):
    def __init__(self):
        self.g1 = Gauge('exchange_rate', 'Exchange rate compared to main currency', ['name'])
        self.g2 = Gauge('exchange_rate_date', 'Exchange rate last updated', ['name'])

class PrometheusController(Controller):
    # TODO(18.0-port): auth='token' is a custom auth type registered by
    # monitoring_prometheus_token_auth (ir.http._auth_method_token), which has no 18.0 source.
    @route("/metrics", auth='token')
    def metrics(self, **kw):
        m = ExchangeRateMetrics()

        currencies = request.env['res.currency'].search([
            ('active', '=', True)
        ])
        for c in currencies:
            # TODO(18.0-port): res.currency 'date' and 'rate' are not listed as removed in
            # OpenUpgrade base 18.0.1.3 analysis, but their presence on 18.0 res.currency was
            # not directly confirmed (OCA 18.0 currency module reads rate_ids[].name).
            if not c['date']:
                continue
            t = time.mktime(c['date'].timetuple())
            m.g1.labels(c['name']).set(c['rate'])
            m.g2.labels(c['name']).set(t)

        headers = {'Content-Type': 'text/plain'}
        return request.make_response(generate_latest(), headers=headers)

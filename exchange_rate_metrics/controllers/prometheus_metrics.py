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
    @route("/metrics", auth='token')
    def metrics(self, **kw):
        m = ExchangeRateMetrics()

        currencies = request.env['res.currency'].search([
            ('active', '=', 'true')
        ])
        for c in currencies:
            if not c['date']:
                continue
            t = time.mktime(c['date'].timetuple())
            m.g1.labels(c['name']).set(c['rate'])
            m.g2.labels(c['name']).set(t)

        headers = {'Content-Type': 'text/plain'}
        return request.make_response(generate_latest(), headers=headers)

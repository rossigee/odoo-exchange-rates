# Copyright 2016-2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from prometheus_client import Gauge, generate_latest

from odoo.http import Controller, route, request

import time

class PrometheusController(Controller):
    _g1 = Gauge('exchange_rate', 'Exchange rate compared to main currency', ['name'])
    _g2 = Gauge('exchange_rate_date', 'Exchange rate last updated', ['name'])

    @route("/metrics", auth='token')
    def metrics(self, **kw):
        currencies = request.env['res.currency'].search([
            ('active', '=', 'true')
        ])
        for c in currencies:
            if not c['date']:
                continue
            t = time.mktime(c['date'].timetuple()) 
            self._g1.labels(c['name']).set(c['rate'])
            self._g2.labels(c['name']).set(t)

        headers = {'Content-Type': 'text/plain'}
        return request.make_response(generate_latest(), headers=headers)

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

    def _metrics_user_id(self):
        """Return the user id for a valid 'metrics'-scoped API key, else False.

        Odoo 18.0 keeps API keys in res.users.apikeys; the scope check is done
        by _check_credentials. Served on its own path because monitoring_prometheus
        already serves /metrics publicly.
        """
        header = request.httprequest.headers.get('Authorization', '')
        if not header.lower().startswith('bearer '):
            return False
        key = header[7:].strip()
        if not key:
            return False
        return request.env['res.users.apikeys'].sudo()._check_credentials(scope='metrics', key=key)

    @route("/metrics/exchange_rates", auth='public', methods=['GET'])
    def metrics(self, **kw):
        uid = self._metrics_user_id()
        if not uid:
            return request.make_response(
                'Unauthorized',
                headers=[('WWW-Authenticate', 'Bearer'), ('Content-Type', 'text/plain')],
                status=401,
            )
        request.update_env(user=uid)

        m = ExchangeRateMetrics()

        currencies = request.env['res.currency'].search([
            ('active', '=', True)
        ])
        for c in currencies:
            # res.currency.date, rate and rate_ids exist in Odoo 18.0 (base/models/res_currency.py).
            if not c['date']:
                continue
            t = time.mktime(c['date'].timetuple())
            m.g1.labels(c['name']).set(c['rate'])
            m.g2.labels(c['name']).set(t)

        headers = {'Content-Type': 'text/plain'}
        return request.make_response(generate_latest(), headers=headers)

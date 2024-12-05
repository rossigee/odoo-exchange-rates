# Copyright 2023 Ross Golder (https://golder.org)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Exchange Rate Metrics',
    'version': '14.0.1.0.1',
    'author': 'Ross Golder',
    'website': 'https://golder.org/',
    'license': 'AGPL-3',
    'category': 'Accounting',
    'summary': 'Provides metrics to monitor exchange rates via Prometheus',
    'depends': [
        'monitoring_prometheus_token_auth',
    ],
    'installable': True,
}

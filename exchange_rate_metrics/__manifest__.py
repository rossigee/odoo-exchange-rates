# Copyright 2023 Ross Golder (https://golder.org)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Exchange Rate Metrics',
    'version': '18.0.1.0.1',
    'author': 'Ross Golder',
    'website': 'https://golder.org/',
    'license': 'AGPL-3',
    'category': 'Accounting',
    'summary': 'Provides metrics to monitor exchange rates via Prometheus',
    # TODO(18.0-port): depends on monitoring_prometheus (18.0, odoo-cloud-platform), which has no
    # token auth. The controller still uses auth='token' from the removed module; token auth must
    # be re-implemented or the route will fail. Decision pending.
    'depends': [
        'monitoring_prometheus',
    ],
    'installable': True,
}

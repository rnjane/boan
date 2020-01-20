"""
Calculates the on-demand rate for the chosen IBM instance type.

Rate is displayed in the time units chosen in Rates Options. Assumes the
currency is USD, edit this action to change it.

This file is applied when provisioning a server.
These rates are updated regularly by the 'Refresh Server Rates' recurring job.
"""


from decimal import Decimal
import os.path
import ijson
import json
import time
import re
import requests

from multiprocessing import Process, Queue

from django.conf import settings
from django.core.cache import cache

import SoftLayer

from costs.utils import default_compute_rate
from resourcehandlers.aws.aws_wrapper import get_region_title
from resourcehandlers.aws.models import AWSHandler
from utilities.filesystem import mkdir_p
from utilities.logger import ThreadLogger
from utilities.models import GlobalPreferences

NUMBER_OF_HOURS = {
    "HOUR": 1,
    "DAY": 24,
    "WEEK": 192,
    "MONTH": 720,  # assumes 30-day month
    "YEAR": 8760,  # assumes 365-day year
}

logger = ThreadLogger(__name__)

def get_client(environment):
    resource_handler = environment.resource_handler
    api_kwargs = {
        "username": resource_handler.serviceaccount,
        "api_key": str(resource_handler.servicepasswd),
    }
    client = SoftLayer.create_client_from_env(**api_kwargs)
    return client

def get_price(environment, cpus, memory):
    client = get_client(environment)
    manager = SoftLayer.OrderingManager(client)
    if cpus == 1:
        cpu = 'GUEST_CORE_' + str(cpus)
    else:
        cpu = 'GUEST_CORES_' + str(cpus)
    memory = 'RAM_' + str(memory) +'_GB'

    try:
        location_groups = [data_center['groups'] for data_center in client.call('SoftLayer_Location', 'getDatacenters', mask='groups') if data_center['name'] == environment.slayer_datacenter]
        location_group_ids = []
        for location_group in location_groups:
            for location in location_group:
                location_group_ids.append(location['id'])

        item_prices = client.call('SoftLayer_Product_Package', 'getItemPrices', id=835)

        cpu_cost = [float(cost['hourlyRecurringFee']) for cost in item_prices if (cost['locationGroupId'] in location_group_ids and cost['item'].get('keyName') == cpu)][0]
        memory_cost = [float(cost['hourlyRecurringFee']) for cost in item_prices if (cost['locationGroupId'] in location_group_ids and cost['item'].get('keyName') == memory)][0]
        total_cost = cpu_cost + memory_cost
        return total_cost
    except Exception as e:
        print('-------------------------')
        print(e)
        return 0

def compute_rate(group, environment, resource_technology, cfvs, pcvss,
                 os_build, apps, quantity=1, **kwargs):

    override_defaults = kwargs.pop("override_defaults", False)

    if override_defaults:
        # This is also useful for testing to check whether we returned rates just from IBM.
        logger.info(f"Only including IBM-specific rates from the IBM rate hook.")
        rate_dict = {}
    else:
        # The rate_dict below will include any Software or Extra rates from the Admin/Rates settings.
        # You can modify this file to exclude these rates.
        rate_dict = default_compute_rate(
            group,
            environment,
            resource_technology,
            cfvs,
            pcvss,
            os_build,
            apps,
            quantity,
            **kwargs,
        )
        # Override Hardware rates for consistency; so that we don't return the
        # default CPU/Disk Rates, which would be misleading about whether we got the
        # rate from IBM.
        rate_dict.update({"Hardware": {}})
        logger.info(f"Including the default Admin/rates in the IBM rate hook.")

    server_preset = []
    for cfv in cfvs:
        if cfv.field.name == 'cpu_cnt':
            cpus = cfv.value
        if cfv.field.name == 'mem_size':
            memory = cfv.value
    rate = get_price(environment, cpus, memory)

    rate_time_unit = GlobalPreferences.objects.get().rate_time_unit
    number_of_hours = NUMBER_OF_HOURS.get(rate_time_unit, 0)
    rate_dict.update({
        "Hardware": {
            "Instance Type": Decimal(rate)
        },
    })
    return rate_dict

# [p for p in manager.get_item_prices(835) if (p['locationGroupId'] is not None and p['item'].get('units') == 'CORE')]
# [preset for preset in client.call('SoftLayer_Product_Package_Preset', 'getAllObjects') if (preset['keyName'].startswith("B1") and preset['keyName'].endswith('25'))]

# mlist = []
# for i in [k['groups'] for k in client.call('SoftLayer_Location', 'getDatacenters', mask='groups') if k['name'] == 'ams01']:
#     for l in i:
#         mlist.append(l['id'])

# item_prices = client.call('SoftLayer_Product_Package', 'getItemPrices', id=835, filter={"locationgroupid": 503})

# cpu_cost = [float(p['hourlyRecurringFee']) for p in item_prices if (p['locationGroupId'] in [68, 2, 503] and p['item'].get('keyName') == 'GUEST_VCORE_2')]
# memory_cost = [float(p['hourlyRecurringFee']) for p in item_prices if (p['locationGroupId'] in [68, 2, 503] and p['item'].get('keyName') == 'RAM_2_GB')][0]

# cpu_cost = [float(p['hourlyRecurringFee']) for p in item_prices if (p['locationGroupId'] in [68, 2, 503] and p['item'].get('keyName') == 'GUEST_4_VCORES')][0]
# memory_cost = [float(p['hourlyRecurringFee']) for p in item_prices if (p['locationGroupId'] in [68, 2, 503] and p['item'].get('keyName') == 'RAM_8_GB')][0]

# print(cpu_cost + memory_cost)

# def x():
#     for preset in presets:
#             if [int(server_value) for server_value in preset['keyName'].split('_')[1].split('X')[:2]] == server_values:
#                 print(sum([float(price['hourlyRecurringFee']) for price in manager.get_preset_prices(preset['id'])['prices']]))
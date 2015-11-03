# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import logging
import os

import staticconf
from yelp_servlib.config_util import load_default_config


log = logging.getLogger('replication_handler.config')


class BaseConfig(object):
    """Staticconf base object for managing config
    TODO: (cheng|DATAPIPE-88) Removed the config reloading code, will work on that later.
    """

    def __init__(self, config_path='config.yaml', env_config_path='config-env-dev.yaml'):
        SERVICE_CONFIG_PATH = os.environ.get('SERVICE_CONFIG_PATH', config_path)
        SERVICE_ENV_CONFIG_PATH = os.environ.get('SERVICE_ENV_CONFIG_PATH', env_config_path)
        load_default_config(SERVICE_CONFIG_PATH, SERVICE_ENV_CONFIG_PATH)


class EnvConfig(BaseConfig):
    """When we do staticconf.get(), we will get a ValueProxy object, sometimes it is
    not accepted, so by calling value on that we will get its original value."""

    @property
    def rbr_source_cluster(self):
        return staticconf.get('rbr_source_cluster').value

    @property
    def schema_tracker_cluster(self):
        return staticconf.get('schema_tracker_cluster').value

    @property
    def rbr_state_cluster(self):
        return staticconf.get('rbr_state_cluster').value

    @property
    def register_dry_run(self):
        return staticconf.get('register_dry_run').value

    @property
    def publish_dry_run(self):
        return staticconf.get('publish_dry_run').value

    @property
    def topology_path(self):
        return staticconf.get('topology_path').value

    @property
    def schema_blacklist(self):
        return staticconf.get('schema_blacklist').value

    @property
    def table_whitelist(self):
        return staticconf.get('table_whitelist').value

    @property
    def zookeeper_discovery_path(self):
        return staticconf.get('zookeeper_discovery_path').value

    @property
    def producer_name(self):
        return staticconf.get('producer_name').value

    @property
    def team_name(self):
        return staticconf.get('team_name').value

    @property
    def pii_yaml_path(self):
        return staticconf.get('pii_yaml_path').value

    @property
    def max_delay_allowed_in_minutes(self):
        return staticconf.get('max_delay_allowed_in_minutes').value

    @property
    def sensu_host(self):
        return staticconf.get('sensu_host').value


class DatabaseConfig(object):
    """Used for reading database config out of topology.yaml in the environment"""

    def __init__(self, cluster_name, topology_path):
        load_default_config(topology_path)
        self._cluster_name = cluster_name

    @property
    def cluster_config(self):
        for topo_item in staticconf.get('topology'):
            if topo_item.get('cluster') == self.cluster_name:
                return topo_item

    @property
    def entries(self):
        return self.cluster_config['entries']

    @property
    def cluster_name(self):
        return self._cluster_name


env_config = EnvConfig()

source_database_config = DatabaseConfig(
    env_config.rbr_source_cluster,
    env_config.topology_path
)
schema_tracking_database_config = DatabaseConfig(
    env_config.schema_tracker_cluster,
    env_config.topology_path
)

#!/usr/bin/python
#
# Copyright (c) 2017 Zim Kalinowski, <zikalino@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: azure_rm_mysqldatabase_facts
version_added: "2.5"
short_description: Get MySQL Database facts.
description:
    - Get facts of MySQL Database.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    database_name:
        description:
            - The name of the database.

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
  - name: Get instance of MySQL Database
    azure_rm_mysqldatabase_facts:
      resource_group: resource_group_name
      server_name: server_name
      database_name: database_name

  - name: List instances of MySQL Database
    azure_rm_mysqldatabase_facts:
      resource_group: resource_group_name
      server_name: server_name
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.rdbms.mysql import MySQLManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMDatabasesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            server_name=dict(
                type='str',
                required=True
            ),
            database_name=dict(
                type='str',
                required=False
            ),
        )
        # store the results of the module operation
        self.results = dict(
            changed=False,
            ansible_facts=dict()
        )
        self.mgmt_client = None
        self.resource_group = None
        self.server_name = None
        self.database_name = None
        super(AzureRMDatabasesFacts, self).__init__(self.module_arg_spec)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])
        self.mgmt_client = self.get_mgmt_svc_client(MySQLManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        if (self.resource_group is not None and
                self.server_name is not None and
                self.database_name is not None):
            self.results['ansible_facts']['get'] = self.get()
        elif (self.resource_group is not None and
              self.server_name is not None):
            self.results['ansible_facts']['list_by_server'] = self.list_by_server()
        return self.results

    def get(self):
        '''
        Gets facts of the specified MySQL Database.

        :return: deserialized MySQL Databaseinstance state dictionary
        '''
        response = None
        results = False
        try:
            response = self.mgmt_client.databases.get(self.resource_group,
                                                      self.server_name,
                                                      self.database_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Databases.')

        if response is not None:
            results = response.as_dict()

        return results

    def list_by_server(self):
        '''
        Gets facts of the specified MySQL Database.

        :return: deserialized MySQL Databaseinstance state dictionary
        '''
        response = None
        results = False
        try:
            response = self.mgmt_client.databases.list_by_server(self.resource_group,
                                                                 self.server_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Databases.')

        if response is not None:
            results = []
            for item in response:
                results.append(item.as_dict())

        return results


def main():
    AzureRMDatabasesFacts()
if __name__ == '__main__':
    main()
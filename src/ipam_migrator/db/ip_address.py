#
# IPAM database migration script
# ipam_migrator/db/ip/address.py - Internet Protocol (IP) addresses
#
# Copyright (c) 2017 Catalyst.net Ltd
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


'''
Internet Protocol (IP) addresses.
'''


import ipaddress

from ipam_migrator.db.object import Object


class IPAddress(Object):
    '''
    Database type for Internet Protocol (IP) addresses.
    '''

    # pylint: disable=too-many-arguments
    def __init__(self,
                 address_id,
                 address,
                 mask,
                 description=None,
                 custom_fields=None,
                 vrf_id=None,
                 hostname=None):  # Add 'hostname' as an argument
        '''
        VLAN object constructor.
        '''

        # Initialize the database object with ID.
        super().__init__(address_id, None, description)

        # Internal fields.
        self.address = ipaddress.ip_address(address)
        self.family = 6 if isinstance(self.address, ipaddress.IPv6Address) else 4
        self.custom_fields = custom_fields.copy() if custom_fields is not None else dict()

        # Grouping fields, in ascending order of scale.
        self.vrf_id = int(vrf_id) if vrf_id is not None else None
        self.hostname = str(hostname) if hostname is not None else None  # Add 'hostname' field
        self.mask = str(mask)

    def __str__(self):
        '''
        String representation of an IPAddress.
        '''

        if self.description:
            return "IP address {}/{} with description '{}'".format(self.address, self.mask, self.description)
        return "IP address {}".format(self.address)

    def as_dict(self):
        '''
        Dictionary representation of an IPAddress.
        '''
        
         # Replace '/' with '.' in the hostname field
        sanitized_hostname = self.hostname.replace('/', '.') if self.hostname else None

        return {
            "id": self.id_get(),
            "description": self.description,

            "address": str(self.address),
            "family": self.family,
            "custom_fields": self.custom_fields.copy(),

            "vrf_id": self.vrf_id,
            "dns_name": sanitized_hostname,  # Include 'hostname' in the dictionary

            "mask": self.mask
        }

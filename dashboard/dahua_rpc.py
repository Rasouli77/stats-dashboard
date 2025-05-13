#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Basic Dahua RPC wrapper.
Forked from https://github.com/naveenrobo/dahua-ip-cam-sdk.git
Added filtering and retrieving statistics for the count of people who have passed the defined zone
Example:
    from dahua_rpc import DahuaRpc
    dahua = DahuaRpc(host="192.168.1.10", username="admin", password="password")
    dahua.login()
  # Get the current time on the device
    dahua.current_time()
  # Get serial number
    dahua.request(method="magicBox.getSerialNo")
  # Get the people counting statistics for defined area and specific period of time by using the following
    object_id = dahua.get_people_counting_info() # Get the object id
  # Get the total count of the statistics stored for the defined period of time
    totalCount = dahua.start_find_statistics_data(object_id, StartTime, EndTime, AreaID) # Use the object id to find the stored statisics data
  # Get statistics list
    list = dahua.do_find_statistics_data(object_id) # Use the object id to get the statisics data
  # Release token
    dahua.stop_find_statistics_data(object_id) # Use the object id to release filtered data
  # Logout 
    dahua.logout()
Dependencies:
  pip install requests
"""

import sys
import hashlib

import requests
from enum import Enum

if (sys.version_info > (3, 0)):
    unicode = str


class DahuaRpc(object):

    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

        self.s = requests.Session()
        self.session_id = None
        self.id = 0
        self.token = 0
        self.totalCount = 0


    def request(self, method, params=None, object_id=None, extra=None, url=None):
        """Make a RPC request."""
        self.id += 1
        data = {'method': method, 'id': self.id}
        if params is not None:
            data['params'] = params
        if object_id:
            data['object'] = object_id
        if extra is not None:
            data.update(extra)
        if self.session_id:
            data['session'] = self.session_id
        if not url:
            url = "http://{}/RPC2".format(self.host)
        r = self.s.post(url, json=data)
        return r.json()

    def login(self):
        """Dahua RPC login.
        Reversed from rpcCore.js (login, getAuth & getAuthByType functions).
        Also referenced:
        https://gist.github.com/avelardi/1338d9d7be0344ab7f4280618930cd0d
        """

        # login1: get session, realm & random for real login
        url = 'http://{}/RPC2_Login'.format(self.host)
        method = "global.login"
        params = {'userName': self.username,
                  'password': "",
                  'clientType': "Web3.0"}
        r = self.request(method=method, params=params, url=url)

        self.session_id = r['session']
        realm = r['params']['realm']
        random = r['params']['random']

        # Password encryption algorithm
        # Reversed from rpcCore.getAuthByType
        pwd_phrase = self.username + ":" + realm + ":" + self.password
        if isinstance(pwd_phrase, unicode):
            pwd_phrase = pwd_phrase.encode('utf-8')
        pwd_hash = hashlib.md5(pwd_phrase).hexdigest().upper()
        pass_phrase = self.username + ':' + random + ':' + pwd_hash
        if isinstance(pass_phrase, unicode):
            pass_phrase = pass_phrase.encode('utf-8')
        pass_hash = hashlib.md5(pass_phrase).hexdigest().upper()

        # login2: the real login
        params = {'userName': self.username,
                  'password': pass_hash,
                  'clientType': "Web3.0",
                  'loginType': "Direct",
                  'authorityType': "Default"}
        r = self.request(method=method, params=params, url=url)

        if r['result'] is False:
            raise LoginError(str(r))

    def get_product_def(self):
        method = "magicBox.getProductDefinition"

        params = {
            "name" : "Traffic"
        }
        r = self.request(method=method, params=params)

        if r['result'] is False:
            raise RequestError(str(r))

    def keep_alive(self):
        params = {
            'timeout': 300,
            'active': False
        }

        method = "global.keepAlive"
        r = self.request(method=method, params=params)

        if r['result'] is True:
            return True
        else:
            raise RequestError(str(r))

    def get_traffic_info(self):
        method = "RecordFinder.factory.create"

        params = {
            "name" : "TrafficSnapEventInfo"
        }
        r = self.request(method=method, params=params)
        
        if type(r['result']):
            return r['result']
        else:
            raise RequestError(str(r))

    def start_find(self,object_id):
        method = "RecordFinder.startFind"
        object_id = object_id
        params = {
            "condition" : {
                "Time" : ["<>",1558925818,1559012218]
            }
        }
        r = self.request(object_id=object_id,method=method, params=params)

        if r['result'] is False:
            raise RequestError(str(r))

    def do_find(self,object_id):
        method = "RecordFinder.doFind"
        object_id = object_id
        params = {
            "count" : 50000
        }
        r = self.request(object_id=object_id,method=method, params=params)

        if r['result'] is False:
            raise RequestError(str(r))
        else:
            return r
            
    def set_config(self, params):
        """Set configurations."""

        method = "configManager.setConfig"
        r = self.request(method=method, params=params)

        if r['result'] is False:
            raise RequestError(str(r))

    def reboot(self):
        """Reboot the device."""

        # Get object id
        method = "magicBox.factory.instance"
        params = ""
        r = self.request(method=method, params=params)
        object_id = r['result']

        # Reboot
        method = "magicBox.reboot"
        r = self.request(method=method, params=params, object_id=object_id)

        if r['result'] is False:
            raise RequestError(str(r))

    def current_time(self):
        """Get the current time on the device."""

        method = "global.getCurrentTime"
        r = self.request(method=method)
        if r['result'] is False:
            raise RequestError(str(r))

        return r['params']['time']

    def ntp_sync(self, address, port, time_zone):
        """Synchronize time with NTP."""

        # Get object id
        method = "netApp.factory.instance"
        params = ""
        r = self.request(method=method, params=params)
        object_id = r['result']

        # NTP sync
        method = "netApp.adjustTimeWithNTP"
        params = {'Address': address, 'Port': port, 'TimeZone': time_zone}
        r = self.request(method=method, params=params, object_id=object_id)

        if r['result'] is False:
            raise RequestError(str(r))

    def get_split(self):
        """Get display split mode."""

        # Get object id
        method = "split.factory.instance"
        params = {'channel': 0}
        r = self.request(method=method, params=params)
        object_id = r['result']

        # Get split mode
        method = "split.getMode"
        params = ""
        r = self.request(method=method, params=params, object_id=object_id)

        if r['result'] is False:
            raise RequestError(str(r))

        mode = int(r['params']['mode'][5:])
        view = int(r['params']['group']) + 1

        return mode, view

    def attach_event(self, event = []):
        """Attach a event to current session"""
        method = "eventManager.attach"
        if(event is None):
            return
        params = {
            'codes' : [*event]
        }

        r = self.request(method=method, params=params)

        if r['result'] is False:
            raise RequestError(str(r))

        return r['params']


    def listen_events(self, _callback= None):
        """ Listen for envents. Attach an event before using this function """
        url = "http://{host}/SubscribeNotify.cgi?sessionId={session}".format(host=self.host,session=self.session_id)
        response = self.s.get(url, stream= True)

        buffer = ""
        for chunk in response.iter_content(chunk_size=1):
            buffer += chunk.decode("utf-8")
            if (buffer.endswith('</script>') is True):
                if _callback:
                    _callback(buffer)
                buffer = ""

    def set_split(self, mode, view):
        """Set display split mode."""

        if isinstance(mode, int):
            mode = "Split{}".format(mode)
        group = view - 1

        # Get object id
        method = "split.factory.instance"
        params = {'channel': 0}
        r = self.request(method=method, params=params)
        object_id = r['result']

        # Set split mode
        method = "split.setMode"
        params = {'displayType': "General",
                  'workMode': "Local",
                  'mode': mode,
                  'group': group}
        r = self.request(method=method, params=params, object_id=object_id)

        if r['result'] is False:
            raise RequestError(str(r))
        
    def get_people_counting_info(self):
        method = "videoStatServer.factory.instance"

        params = {'channel' : 0}

        r = self.request(method=method, params=params)
        
        if type(r['result']):
            return r['result']
        else:
            raise RequestError(str(r))
    
    def start_find_statistics_data(self, object_id, StartTime, EndTime, AreaID):
        method = "videoStatServer.startFind"                

        params={
            'condition': {
                'StartTime' : StartTime, 
                'EndTime' : EndTime, 
                'Granularity' : "Hour", 
                'RuleType' : "NumberStat", 
                'PtzPresetId' : 0, 
                'AreaID' : [AreaID]
            }
        }

        r = self.request(method=method, params=params,object_id=object_id)

        if r['result'] is False:
            raise RequestError(str(r))
        else:
            self.token = r['params']['token']
            self.totalCount = r['params']['totalCount']

            return self.totalCount
        
    def do_find_statistics_data(self, object_id):
        method = "videoStatServer.doFind"

        params = {
            'token':self.token, 
            'beginNumber' : 0, 
            'count' : self.totalCount
        }

        r = self.request(method=method, params=params,object_id=object_id)

        if r['result'] is False:
            raise RequestError(str(r))
        else:            
            return r['params']['info']            
        
    def stop_find_statistics_data(self, object_id):
        method = "videoStatServer.stopFind"

        params = { 'token' : self.token }

        r = self.request(method=method, params=params,object_id=object_id)

        if r['result'] is False:
            raise RequestError(str(r))
        else:
            self.token = 0
            self.totalCount = 0
            return
    
    def logout(self):
        method = "global.logout"

        params = {}

        r = self.request(method=method, params=params)

        if r['result'] is False:
            raise RequestError(str(r))
        else:
            self.session_id = None
            self.id = 0
            return
    
    def get_area_id_by_rule_name(self, object_id, rule_name, rule_type="NumberStat", channel=0):
        method = "videoAnalyse.getRules"
        params = {
            "channel": channel,
            "RuleType": rule_type
        }

        response = self.request(method=method, params=params, object_id=object_id)

        if not response.get("result"):
            raise Exception(f"API error: {response}")

        for rule in response["params"]["Rules"]:
            if rule.get("Name") == rule_name:
                return rule.get("AreaID")

        raise Exception(f"Rule '{rule_name}' not found.")


class LoginError(Exception):
    pass


class RequestError(Exception):
    pass
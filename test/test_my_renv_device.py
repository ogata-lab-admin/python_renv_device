#!/usr/bin/env python

import unittest, json
from renv_device import RenvDevice, actionHandler, event

class MyRenvDevice(RenvDevice):
    def __init__(self, typeId, name, version, device_uuid, deviceId, devicePass):
        RenvDevice.__init__(self, typeId, name, version, device_uuid, deviceId, devicePass)
        self._msg_buffer = []
        pass
    
    @actionHandler
    def onSetup(self):
        """
        This function is called at first.
        """
        print 'onSetup is called'
        pass

    @actionHandler
    def onEcho(self, value):
        """
        This function echoes the given value
        @param {String} value Echo back value [echo1 : Echo Data 1 | echo2 : Echo Data 2]
        """
        self._msg_buffer.append('MyRenvDevice.onEcho(' + value + ') called.')
        pass

    @event
    def sendEchoBack(self, value):
        """
        This function send back the echo information.
        """
        self._msg_buffer.append('MyRenvDevice.onEchoBack(' + value + ') called.')
        return value
        
    @actionHandler
    def onTestMessage(self, value):
        """
        This is test function.
        @param {Int} value data test value.
        """
        print value
        pass

class TestMyRenvDeviceInfo(unittest.TestCase):
    """test class of tashizan.py
    """

        
            
    def setUp(self):

        self._devTypeId = "WEB.DEVICE.TEST_MY_RENV_DEVICE"
        self._devName = "test_device001"
        self._version = "1.2.3"


        self._devUUID = "uuid-1234-5678-9012"        
        self._devId = "name-renv-device-name-for-test"
        self._devPass = "password001"
        
        self._rd = MyRenvDevice(self._devTypeId, self._devName, self._version, self._devUUID, self._devId, self._devPass)
                                


    def test_givenIdIsEqualToDeviceInfoName(self):
        """
        """
        deviceInfo = self._rd.getDeviceInfo()
        #print deviceInfo
        self.assertEqual(self._devUUID, deviceInfo['deviceId'])
        self.assertEqual(self._devTypeId, deviceInfo['deviceTypeId'])
        self.assertEqual(self._devName + ':' + self._version, deviceInfo['deviceName'])

    def test_DeviceInfoHasCapability(self):
        deviceInfo = self._rd.getDeviceInfo()
        capabilities = deviceInfo['capabilityList']
        foundSetup = False
        foundEcho = False
        foundEchoBack = False
        for c in capabilities:
            if c['eventName'] == 'Setup':
                foundSetup = True
                self.assertEqual(c['eventType'], "In")

            if c['eventName'] == 'Echo':
                foundEcho = True
                self.assertEqual(c['eventType'], "In")

            if c['eventName'] == 'EchoBack':
                foundEchoBack = True
                self.assertEqual(c['eventType'], "Out")
            pass
        self.assertTrue(foundSetup)
        self.assertTrue(foundEcho)
        self.assertTrue(foundEchoBack)
            
        #print deviceInfo


    def test_dispachMessage(self):
        self._rd._dispatch_message(json.dumps({
                "eventName": "Echo",
                "eventParam" : {
                    "value" : {"val" : "test_echo_value01",} }}))




if __name__ == "__main__":
    unittest.main()

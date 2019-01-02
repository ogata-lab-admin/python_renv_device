#!/usr/bin/env python
# -encoding: utf-8 

import os, sys, traceback, logging, codecs, argparse, threading

from logging import getLogger

from renv_device import RenvDevice, actionHandler, event
# sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

logging.basicConfig(filename='example.log',level=logging.DEBUG, format='%(levelname)s:%(asctime)s %(message)s')
logger = getLogger(__name__)

class MyRenvDevice(RenvDevice):
    def __init__(self, deviceUUID, connectionID, connectionPass, logger=logger):
        """
        """
        typeId = 'PYTHON.OGATALAB.EXAMPLE001'
        name   = 'Ogatalab-Example-Device-001'
        version = '1.2.3'
        
        RenvDevice.__init__(self, typeId, name, version, deviceUUID, connectionID, connectionPass, logger=logger)
        self._msg_buffer = []

        # How to append Action Handler manually 
        paramInfo = self.buildParamInfo('arg1', 'String', 'Test argument')
        self.addCustomActionHandler('Echo2', 'Test Command', [paramInfo], self._handler)

        # How to append Event Sender Manually
        paramInfo2 = self.buildParamInfo('arg1', 'String', 'Test Data')
        self.func = self.addCustomEvent('Send1', 'Test Event', [paramInfo2])
        pass

    def _handler(self, arg1):
        print ('MyRenvDevice._handler called')
        print (arg1)
    
    @actionHandler
    def onSetup(self):
        """
        この関数はデバイス側コンソールに文字列を出力するのみです
        """
        print 'onSetup is called'
        pass

    @actionHandler
    def onEcho(self, value):
        """
        Show value to console

        :param String value: Echo value [echo1 : Echo Data 1 | echo2 : Echo Data 2]
        """
        print value
        self._msg_buffer.append('MyRenvDevice.onEcho(' + value + ') called.')
        pass

    @event
    def sendMyEvent01(self, value):
        """
        This function send simple string value to R-env
        
        :return String value: Simple String argument passed to event function
        """
        return {'value': value}
        

def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-u', '--UUID', help='Device Unique ID', type=str, dest='uuid', required=True)
        parser.add_argument('-i', '--connectionID', help='Device Websocket Connection ID', type=str, dest='id', required=True)
        parser.add_argument('-p', '--connectionPassword', help='Device Websocket Connection Password', type=str, dest='password', required=True)
        parser.add_argument('-d', '--deviceServer', help='Device Server URL', type=str, dest='host', required=True)
        parser.add_argument('-n', '--number of port', help='Device Server Port Number', type=str, dest='port', required=True)
        args = parser.parse_args()
        rd = MyRenvDevice(args.uuid, args.id, args.password)
        print('Device Info is')
        print rd.getDeviceInfo()
        rd.connect(args.host + ':' + args.port)
        th = threading.Thread(target=rd.run_forever)
        th.start()
        def show_help():
            print('USAGE:')
            print('  type "quit" to exit.')
        while True:
            c = raw_input('Input Command(type "help" to show help):')
            if len(c.strip()) == 0: continue
            elif c.strip() == 'help': show_help()
            elif c.strip() == 'quit': break
            else:
                rd.sendMyEvent01(c.strip())
        print('Stopping R-env Device Example')
        rd.stop_running()
        #th.join()
        
    except:
        print('Error Traced')
        traceback.print_exc()
        
        sys.exit(-1)
    
    
if __name__ == '__main__':
    main()


'''
Created on May 27, 2016

@author: root
'''
import unittest
import sys
from oslo.config import cfg
import cloudkitty.collector
from stevedore import driver
from stevedore import extension
from cloudkitty.collector.ceilometer import CeilometerCollector as collector

FETCHERS_NAMESPACE = 'cloudkitty.tenant.fetchers'
COLLECTORS_NAMESPACE = 'cloudkitty.collector.backends'
FETCHERS_NAMESPACE = 'cloudkitty.tenant.fetchers'
TRANSFORMERS_NAMESPACE = 'cloudkitty.transformers'
PROCESSORS_NAMESPACE = 'cloudkitty.rating.processors'
STORAGES_NAMESPACE = 'cloudkitty.storage.backends'

CONF = cfg.CONF
CONF.import_opt('backend', 'cloudkitty.storage', 'storage')
CONF.import_opt('backend', 'cloudkitty.tenant_fetcher', 'tenant_fetcher')

class Test(unittest.TestCase):

    def setUp(self):
        #start=1464525000,end=1464525060,project_id=982ea1a1fa2f4efda4a89bee11425c75,q_filter=None
        #func = getattr(self, 'get_bandwidth')
        print sys._getframe().f_code.co_name
        self.transformers = {}
        self._load_transformers()

        self.collector_args = {'transformers': self.transformers,
                          'period': '60'}
        #col = collector(collector_args,{'period': '60'})
        #raw_data = col.get_bandwidth('1464525000', '1464525060', '982ea1a1fa2f4efda4a89bee11425c75', None)
        self.collector = driver.DriverManager(
            COLLECTORS_NAMESPACE,
            CONF.collect.collector,
            invoke_on_load=True,
            invoke_kwds=self.collector_args).driver
        pass
        
    def tearDown(self):
        pass


    def test_get_bandwidth(self):
        print sys._getframe().f_code.co_name
        check_dt={}
        #raw_data =func( '1464525000', '1464525060', '982ea1a1fa2f4efda4a89bee11425c75', None)
        check_dt= self.collector.retrieve('bandwidth','1464515000','1464519060')
        
        vol = check_dt['bandwidth'][0]
        self.assertIsNotNone(vol,'is none')
        #self.assertEqual(calc_dt, check_dt)

    def test_get_network_bw_lbs_in(self):
        print sys._getframe().f_code.co_name
        check_dt={}
        #raw_data =func( '1464525000', '1464525060', '982ea1a1fa2f4efda4a89bee11425c75', None)
        check_dt= self.collector.retrieve('network.bw.lbs.in','1464515000','1464519060')
        
        vol = check_dt['network.bw.lbs.in'][0]
        print vol
        self.assertIsNotNone(vol,'is none')
        #self.assertEqual(calc_dt, check_dt)

    def test_get_network_bw_lbs_out(self):
        print sys._getframe().f_code.co_name
        check_dt={}
        #raw_data =func( '1464525000', '1464525060', '982ea1a1fa2f4efda4a89bee11425c75', None)
        check_dt= self.collector.retrieve('network.bw.lbs.out','1464515000','1464519060')
        
        vol = check_dt['network.bw.lbs.out'][0]
        print vol
        self.assertIsNotNone(vol,'is none')
        #self.assertEqual(calc_dt, check_dt)
        
    def test_get_network_bw_lbs_pool(self):
        print sys._getframe().f_code.co_name
        check_dt={}
        #raw_data =func( '1464525000', '1464525060', '982ea1a1fa2f4efda4a89bee11425c75', None)
        check_dt= self.collector.retrieve('network.bw.lbs.pool','1464515000','1464519060')
        
        vol = check_dt['network.bw.lbs.pool'][0]
        print vol
        self.assertIsNotNone(vol,'is none')
        #self.assertEqual(calc_dt, check_dt)
        
    def test_get_snapshot(self):
        print sys._getframe().f_code.co_name
        check_dt={}
        #raw_data =func( '1464525000', '1464525060', '982ea1a1fa2f4efda4a89bee11425c75', None)
        check_dt= self.collector.retrieve('snapshot','1464515000','1464519060')
        
        vol = check_dt['snapshot'][0]
        print vol
        self.assertIsNotNone(vol,'is none')
        #self.assertEqual(calc_dt, check_dt)
        
    def test_get_snapshot_size(self):
        print sys._getframe().f_code.co_name
        check_dt={}
        #raw_data =func( '1464525000', '1464525060', '982ea1a1fa2f4efda4a89bee11425c75', None)
        check_dt= self.collector.retrieve('snapshot.size','1464515000','1464519060')
        
        vol = check_dt['snapshot.size'][0]
        print vol
        self.assertIsNotNone(vol,'is none')
        #self.assertEqual(calc_dt, check_dt)


    def _load_transformers(self):
        self.transformers = {}
        transformers = extension.ExtensionManager(
            TRANSFORMERS_NAMESPACE,
            invoke_on_load=True)

        for transformer in transformers:
            t_name = transformer.name
            t_obj = transformer.obj
            self.transformers[t_name] = t_obj

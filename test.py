import unittest
from collections import Counter

from server import ListServer, Product, Client, MapServer

server_types = (ListServer, MapServer)





class ServerTest(unittest.TestCase):
    ls = ListServer([Product('AB123', 123), Product('abd123', 1000),Product('abc122',1000)],3)
    ls2= ListServer([Product('AB123', 123), Product('abd123', 1234),Product('abc12',1000)],0)
    ds = MapServer([Product('abd123', 1000), Product('Abd123', 2000),Product('abc12',0)],3)
    ds2 = MapServer([Product('ABc123', 123), Product('abd123', 1234), Product('abc12', 1000)])
    def test_List(self):

        self.assertEqual(self.ls.n_max_returned_entries,3)
    def test_map(self):

        self.assertEqual(self.ds.n_max_returned_entries,3)
        self.assertEqual(self.ds.product_dict['abd123'],1000)
    def test_get_entires_listserver(self):
        self.assertEqual(self.ls.get_entries(3)[0].name,'abd123')
    def test_get_entires_mapserver(self):
        self.assertEqual(self.ds.get_entries(3)[0].name, 'abd123')
    def test_get_total_price(self):
        c=Client(self.ls)
        cd=Client(self.ds)
        cd2=Client(self.ds2)
        cd_with_exepition=Client(self.ls2)
        self.assertEqual(c.get_total_price(3),2000)
        self.assertEqual(cd.get_total_price(3), 3000)
        self.assertEqual(c.get_total_price(2), 123)
        self.assertEqual(cd.get_total_price(2), None)
        self.assertEqual(cd2.get_total_price(2), None)
        self.assertEqual(cd_with_exepition.get_total_price(2), None)





class ClientTest(unittest.TestCase):
        def test_total_price_for_normal_execution(self):
            products = [Product('PP234', 2), Product('PP235', 3)]
            for server_type in server_types:
                server = server_type(products)
                client = Client(server)
                self.assertEqual(5, client.get_total_price(2))
if __name__ == '__main__':
    unittest.main()

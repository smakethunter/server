#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from abc import ABC, abstractmethod
from typing import Optional,List, Dict
import unittest
#deklaracja maksymaclnej dlugosci
#Wojciech Pełka i Konrad Stalmach

MAX=100

class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)
    def __init__(self, product_: str, price_: float = 0):
        self.name = product_
        self.price = price_


    pass

# Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
class TooManyProductsFoundError(Exception):
    def _init__(self, number_of_products: int):
        self.supr=number_of_products
        self.over_supr=number_of_products - self.supr

    def __str__(self):
        return f"too much products {self.over_supr}, max is : {self.supr}"

    pass


# FIXME: Każada z poniższych klas serwerów powinna posiadać: (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product`
#  i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#  (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną
#  liczbę wyników wyszukiwania,
#  (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania
product_l= List[Product]

class Server(ABC):
    def __init__(self,max=1):
        self.n_max_returned_entries = max
        pass
        self.n_max_returned_entries=max
    @abstractmethod
    def get_entries(self,n_letters:int):
        pass
    pass
class ListServer(Server):
    def __init__(self, product_list: product_l,max=0):
        self.products: List[Product] = product_list
        super().__init__(max)


    def get_entries(self, n_letters:int)->product_l:
        matching_list:product_l=[]
        matching_letters= n_letters * '[a-zA-Z]'
        matching_letters2 = matching_letters + "[0-9][0-9][0-9]$"
        matching_letters=matching_letters + "[0-9][0-9]$"

        try:
            for product in self.products:


                if re.match(matching_letters,product.name) or re.match(matching_letters2,product.name):
                    matching_list.append(product)
                if len(matching_list)>self.n_max_returned_entries:
                    matching_list=[]
                    raise TooManyProductsFoundError(len(matching_list),self.n_max_returned_entries)

        finally: return matching_list


        pass

    pass


class MapServer(Server):
    product_dict=None
    def __init__(self, product_list :product_l,max=0):
        self.product_dict={}
        super().__init__(max)
        for product in product_list:
            self.product_dict[product.name]= product.price


    def get_entries(self, n_letters:int)->product_l:
        matching_list: product_l = []
        matching_letters = n_letters * '[a-zA-Z]'
        matching_letters2 = matching_letters + "[0-9][0-9][0-9]$"
        matching_letters = matching_letters + "[0-9][0-9]$"

        try:
            for product, price in self.product_dict.items():

                if re.match(matching_letters, product) or re.match(matching_letters2, product):
                    matching_list.append(Product(product,price))
                if len(matching_list)>self.n_max_returned_entries:
                    raise TooManyProductsFoundError(len(matching_list),self.n_max_returned_entries)
        finally: return matching_list
        pass
    pass


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer
    def __init__(self, server_:Server):
        self.server=server_


    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        return sum([n.price for n in self.server.get_entries(n_letters)]) if self.server.get_entries(n_letters) else None



class ServerTest(unittest.TestCase):
    ls = ListServer([Product('AB123', 123), Product('abd123', 1234),Product('abc12',1000)],3)
    ls2= ListServer([Product('AB123', 123), Product('abd123', 1234),Product('abc12',1000)],0)
    ds = MapServer([Product('ABc123', 123), Product('abd123', 1234),Product('abc12',1000)],3)
    ds2 = MapServer([Product('ABc123', 123), Product('abd123', 1234), Product('abc12', 1000)], 1)
    def test_List(self):

        self.assertEqual(self.ls.n_max_returned_entries,3)
    def test_map(self):

        self.assertEqual(self.ds.n_max_returned_entries,3)
        self.assertEqual(self.ds.product_dict['ABSSasjnd123'],123)
    def test_get_entires_listserver(self):
        self.assertEqual(self.ls.get_entries(3)[0].name,'abd123')
    def test_get_entires_mapserver(self):
        self.assertEqual(self.ds.get_entries(3)[0].name, 'abd123')
    def test_get_total_price(self):
        c=Client(self.ls)
        cd=Client(self.ds)
        cd_with_exepition=Client(self.ls2)
        self.assertEqual(c.get_total_price(3),2357)
        self.assertEqual(cd.get_total_price(3), 2357)
        self.assertEqual(c.get_total_price(2), 123)
        self.assertEqual(cd.get_total_price(2), None)
        self.assertEqual(cd_with_exepition.get_total_price(2), None)

    def test_exeption(self):
       self.assertRaises(TooManyProductsFoundError, self.ds2.get_entries(3))
if __name__ == '__main__':
    unittest.main()

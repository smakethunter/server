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
    def __init__(self, max:int,current:int):
        self.max=max
        self.current=current
    def __str__(self):
        return f"Too many arguments max: {self.max} but  {self.current} given"
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

    @abstractmethod
    def get_entries(self,n_letters:int):
        pass
    pass
class ListServer(Server):
    def __init__(self, product_list: product_l,max=5):
        self.products: List[Product] = product_list
        super().__init__(max)
    def __str__(self):
        return f"{self.products}"

    def get_entries(self, n_letters:int)->product_l:
        matching_list:product_l=[]
        matching_letters= n_letters * '[a-zA-Z]'
        matching_letters2 = matching_letters + "[0-9][0-9][0-9]$"
        matching_letters1=matching_letters + "[0-9][0-9]$"

        for product in self.products:
            try:
                if len(matching_list)>self.n_max_returned_entries:

                    raise TooManyProductsFoundError(self.n_max_returned_entries, len(matching_list))
                if re.match(matching_letters1,product.name) or re.match(matching_letters2,product.name):
                    matching_list.append(product)

            except TooManyProductsFoundError as TPE:
                matching_list=[]
                print(TPE)

        return matching_list


        pass

    pass


class MapServer(Server):
    product_dict=None
    def __init__(self, product_list :product_l,max=5,*args,**kwargs):
        self.product_dict={}
        super().__init__(max)
        for product in product_list:
            self.product_dict[product.name]= product.price

    def __str__(self):
        return f"{self.product_dict}"
        pass

    def get_entries(self, n_letters:int)->product_l:
        matching_list: product_l = []
        matching_letters = n_letters * '[a-zA-Z]'
        matching_letters2 = matching_letters + "[0-9][0-9][0-9]$"
        matching_letters1 = matching_letters + "[0-9][0-9]$"


        for product, price in self.product_dict.items():
            try:
                if len(matching_list)>self.n_max_returned_entries:

                    raise TooManyProductsFoundError(self.n_max_returned_entries, len(matching_list))

                if re.match(matching_letters1, product) or re.match(matching_letters2, product):
                    matching_list.append(Product(product,price))

            except TooManyProductsFoundError as TPE:
                print(TPE)
                matching_list=[]




        return matching_list

class Client:

    def __init__(self, server_:Server):
        self.server=server_


    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        return sum([n.price for n in self.server.get_entries(n_letters)]) if self.server.get_entries(n_letters) else None








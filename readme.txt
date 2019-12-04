@startuml
class Product {
+__init__(self, product_: str, price_: float)
+ name: product
+ price_: price
}
class TooManyProductsFoundError
{
+__init__(self, max:int,current:int)
+max=max
+current=current
+ __str__(self)

}
class Server{
+__init__(self,max)
+{abstract}get_entries(self,n_letters:int)
+max: int
}

class ListServer {
+__init__(self, product_list: product_l,max:int)
+max:int
+product_list: product_l
+__str__(self)
+ get_entries(self, n_letters:int): product_l
}


class MapServer {
+ __init__(self, product_list :product_l,max:int)
+max:int
+product_list: product_l

}

class Client {
+__init__(self, server_:Server)
+server:Server
+get_total_price(self, n_letters: Optional[int])  :  float
}

ListServer*-- Server
MapServer*-- Server
Client*-- Server
Server*-- Product
TooManyProductsFoundError *-- Product
@enduml

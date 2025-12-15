from typing import List, Tuple, Dict
from collections import defaultdict

from bills.item import Product, Bill
from bills.entity import Buyer, Seller


class OrderType:
    # Do not change this enum
    ASC = 0
    DES = 1


class Statistics:
    def __init__(self, bills: list[Bill]):
        # Do not change this method
        self.bills = bills

    def find_top_sell_product(self) -> Tuple[Product, int]:
        """
        Producto más vendido = el que más veces aparece en todas las facturas.
        Devuelve (Product, apariciones)
        """
        counts: Dict[Product, int] = defaultdict(int)

        for bill in self.bills:
            for product in bill.products:
                counts[product] += 1

        if not counts:
            raise ValueError("No hay productos en las facturas.")

        top_product = max(counts, key=counts.get)
        return top_product, counts[top_product]

    def find_top_two_sellers(self) -> List[Seller]:
        """
        Devuelve hasta 2 vendedores con mayor importe total de ventas.
        Ordenados de mayor a menor.
        """
        totals_by_seller: Dict[str, float] = defaultdict(float)
        seller_ref: Dict[str, Seller] = {}

        for bill in self.bills:
            sid = bill.seller.dni
            seller_ref[sid] = bill.seller
            totals_by_seller[sid] += bill.calculate_total()

        ordered = sorted(totals_by_seller.items(), key=lambda kv: kv[1], reverse=True)
        top_ids = [sid for sid, _ in ordered[:2]]
        return [seller_ref[sid] for sid in top_ids]

    def find_buyer_lowest_total_purchases(self) -> Tuple[Buyer, float]:
        """
        Comprador con menor importe total de compras.
        Devuelve (Buyer, total_compras)
        """
        totals_by_buyer: Dict[str, float] = defaultdict(float)
        buyer_ref: Dict[str, Buyer] = {}

        for bill in self.bills:
            bid = bill.buyer.dni
            buyer_ref[bid] = bill.buyer
            totals_by_buyer[bid] += bill.calculate_total()

        if not totals_by_buyer:
            raise ValueError("No hay compras registradas en las facturas.")

        lowest_id, lowest_total = min(totals_by_buyer.items(), key=lambda kv: kv[1])
        return buyer_ref[lowest_id], float(lowest_total)

    def order_products_by_tax(self, order_type: OrderType) -> List[Tuple[Product, float]]:
        """
        Devuelve una lista ORDENADA de productos ÚNICOS (por product_id),
        ordenados por la suma TOTAL de impuestos (acumulada) del producto.

        Retorna: [(Product, total_impuestos_acumulados), ...]
        """
        totals_by_product_id: Dict[str, float] = defaultdict(float)
        product_ref: Dict[str, Product] = {}

        for bill in self.bills:
            for product in bill.products:
                pid = product.product_id
                product_ref[pid] = product
                totals_by_product_id[pid] += float(product.calculate_total_taxes())

        product_tax_pairs: List[Tuple[Product, float]] = [
            (product_ref[pid], float(total_tax))
            for pid, total_tax in totals_by_product_id.items()
        ]

        # Orden determinista: primero por total impuestos y luego por product_id
        if order_type == OrderType.DES:
            product_tax_pairs.sort(key=lambda pair: (pair[1], pair[0].product_id), reverse=True)
        else:
            product_tax_pairs.sort(key=lambda pair: (pair[1], pair[0].product_id))

        return product_tax_pairs

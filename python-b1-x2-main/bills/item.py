from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List

from .entity import Buyer, Seller

ISD_FACTOR = 0.25


class TaxType(Enum):
    IVA = "IVA"
    ISD = "ISD"


class OrderType(Enum):
    ASC = "ASC"
    DESC = "DESC"


@dataclass(frozen=True)
class Tax:
    tax_id: str
    tax_type: TaxType
    percentage: float  # Ej: 0.12 para 12%


class Product:
    def __init__(
        self,
        product_id: str,
        name: str,
        expiration_date: datetime,
        bar_code: str,
        quantity: int,
        price: float,
        taxes: List[Tax]
    ) -> None:
        self.product_id = product_id
        self.name = name
        self.expiration_date = expiration_date
        self.bar_code = bar_code
        self.quantity = quantity
        self.price = price
        self.taxes = taxes if taxes is not None else []

    def __repr__(self) -> str:
        return f"Product(product_id={self.product_id!r}, name={self.name!r})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Product) and self.product_id == other.product_id

    def __hash__(self) -> int:
        return hash(self.product_id)

    def calculate_tax(self, tax: Tax) -> float:
        """
        Base = quantity * price
        Impuesto = base * percentage
        - Filtra por tipo (IVA o ISD) usando tax.tax_type
        - Para ISD: multiplicar además por ISD_FACTOR (0.25)
        """
        base = float(self.quantity) * float(self.price)
        total = 0.0

        for t in self.taxes:
            if t.tax_type == tax.tax_type:
                value = base * float(t.percentage)
                if t.tax_type == TaxType.ISD:
                    value *= ISD_FACTOR
                total += value

        return float(total)

    def calculate_total_taxes(self) -> float:
        """
        Suma total de impuestos incluidos en self.taxes,
        reutilizando calculate_tax(tax) por tipo.
        """
        # Sumamos por tipo, para reutilizar la lógica del ISD_FACTOR correctamente
        total = 0.0
        for tax_type in {t.tax_type for t in self.taxes}:
            dummy = Tax(tax_id="__dummy__", tax_type=tax_type, percentage=0.0)
            total += self.calculate_tax(dummy)
        return float(total)

    def calculate_total(self) -> float:
        """
        Total producto = (quantity * price) + total_impuestos
        """
        base = float(self.quantity) * float(self.price)
        return float(base + self.calculate_total_taxes())


class Bill:
    def __init__(
        self,
        bill_id: str,
        sale_date: datetime,
        seller: Seller,
        buyer: Buyer,
        products: List[Product]
    ) -> None:
        self.bill_id = bill_id
        self.sale_date = sale_date
        self.seller = seller
        self.buyer = buyer
        self.products = products if products is not None else []

    def __repr__(self) -> str:
        return f"Bill(bill_id={self.bill_id!r})"

    def calculate_total(self) -> float:
        """
        Total factura = suma del total de cada producto.
        """
        return float(sum(p.calculate_total() for p in self.products))

from bills import *
from datetime import date

# Do not change the follwing class


class BillManager:

    def create_buyer_B101(self) -> Buyer:
        return Buyer(dni="B101", email="b101@uoc", mobile="720 988 494", full_name="Bob Zion Owen", age=42, address="Madrid")

    def create_buyer_B102(self) -> Buyer:
        return Buyer(dni="B102", email="b102@uoc", mobile="663 204 507 ", full_name="Javier Leighton Buchanan", age=27, address="Zaragoza")

    def create_buyer_B103(self) -> Buyer:
        return Buyer(dni="B103", email="b103@uoc", mobile="798 403 956 ", full_name="Gia Jaylen Robbins", age=24, address="Barcelona")

    def create_seller_S501(self) -> Seller:
        return Seller(dni="S501", email="s501@uoc", mobile="630 865 173 ", bussines_name="Magical Moments", bussines_address="Madrid")

    def create_seller_S502(self) -> Seller:
        return Seller(dni="S502", email="s502@uoc", mobile="753 565 602 ", bussines_name="Stitch & Sparkle", bussines_address="Murcia")

    def create_seller_S503(self) -> Seller:
        return Seller(dni="S503", email="s503@uoc", mobile="602 581 150 ", bussines_name="Nectarine Natural Candles", bussines_address="Valcenia")

    def create_seller_S504(self) -> Seller:
        return Seller(dni="S504", email="s504@uoc", mobile="786 892 922 ", bussines_name="Draw and Paw", bussines_address="Barcelona")

    def create_seller_S505(self) -> Seller:
        return Seller(dni="S505", email="s505@uoc", mobile="798 403 956 ", bussines_name="Vegan Gains Gym", bussines_address="Barcelona")

    def create_tax_T901T902(self) -> list:
        list_taxes = []
        list_taxes.append(
            Tax(tax_id="T901", tax_type=TaxType.IVA, percentage=0.5))
        list_taxes.append(
            Tax(tax_id="T902", tax_type=TaxType.ISD, percentage=0.5))
        return list_taxes

    def create_tax_T903T904(self) -> list:
        list_taxes = []
        list_taxes.append(
            Tax(tax_id="T903", tax_type=TaxType.IVA, percentage=0.80))
        list_taxes.append(
            Tax(tax_id="T904", tax_type=TaxType.ISD, percentage=0.40))
        return list_taxes

    def create_tax_T905(self) -> list:
        list_taxes = []
        list_taxes.append(
            Tax(tax_id="T905", tax_type=TaxType.IVA, percentage=0.43))
        return list_taxes

    def create_tax_T906(self) -> list:
        list_taxes = []
        list_taxes.append(
            Tax(tax_id="T906", tax_type=TaxType.IVA, percentage=0.75))
        return list_taxes

    def create_tax_T907T908(self) -> list:
        list_taxes = []
        list_taxes.append(
            Tax(tax_id="T907", tax_type=TaxType.IVA, percentage=0.99))
        list_taxes.append(
            Tax(tax_id="T908", tax_type=TaxType.ISD, percentage=0.21))
        return list_taxes

    def create_product_P701(self, quantity) -> Product:
        return Product("P701", "Gadget Genie", date.today(), "ABC-abc-1234-1", quantity, 10, taxes=self.create_tax_T901T902())

    def create_product_P702(self, quantity) -> Product:
        return Product("P702", "Flavor Fusions", date.today(), "ABC-abc-1234-2", quantity, 5.15, taxes=self.create_tax_T903T904())

    def create_product_P703(self, quantity) -> Product:
        return Product("P703", "Taste Treats", date.today(), "ABC-abc-1234-3", quantity, 8, taxes=self.create_tax_T905())

    def create_product_P704(self, quantity) -> Product:
        return Product("P704", "Eco-Friendly Elixirs", date.today(), "ABC-abc-1234-4", quantity, 12, taxes=self.create_tax_T906())

    def create_product_P705(self, quantity) -> Product:
        return Product("P705", "Freshly Foundation", date.today(), "ABC-abc-1234-5", quantity, 3, taxes=self.create_tax_T907T908())

    def create_product_P706(self, quantity) -> Product:
        return Product("P706", "Cleaning Confections", date.today(), "ABC-abc-1234-6", quantity, 55, taxes=self.create_tax_T901T902())

    def create_bills_EX101(self):
        """Create a new bill with a single item for a single client.        
        """
        list_bills = []
        bill = Bill(bill_id="FX101", sale_date=date.today(), seller=self.create_seller_S501(
        ), buyer=self.create_buyer_B101(), products=[self.create_product_P701(10)])
        list_bills.append(bill)
        return list_bills

    def create_bills_EX102(self):
        """Create a two bills with a two items for a single client.        
        """
        list_bills = []
        bill = Bill(bill_id="FX101", sale_date=date.today(), seller=self.create_seller_S501(
        ), buyer=self.create_buyer_B101(), products=[self.create_product_P701(10), self.create_product_P702(10), self.create_product_P705(30)])
        bill = Bill(bill_id="FX102", sale_date=date.today(), seller=self.create_seller_S501(
        ), buyer=self.create_buyer_B101(), products=[self.create_product_P702(8), self.create_product_P704(20)])
        list_bills.append(bill)
        return list_bills

    def create_bills_EX103(self):
        """Create a two bills with a two items for two clients.
        """
        list_bills = []
        bill_B101 = Bill(bill_id="FX101", sale_date=date.today(), seller=self.create_seller_S501(
        ), buyer=self.create_buyer_B101(), products=[self.create_product_P701(10)])
        bill_B102 = Bill(bill_id="FX102", sale_date=date.today(), seller=self.create_seller_S501(
        ), buyer=self.create_buyer_B102(), products=[self.create_product_P702(8)])
        list_bills.append(bill_B101)
        list_bills.append(bill_B102)
        return list_bills

    def create_bills_EX104(self):
        """Create a bill multiple items and buyers
        """
        list_bills = []
        bill_B101 = Bill(bill_id="FX101", sale_date=date.today(), seller=self.create_seller_S501(
        ), buyer=self.create_buyer_B101(), products=[self.create_product_P701(1)])
        bill_B102 = Bill(bill_id="FX102", sale_date=date.today(), seller=self.create_seller_S501(
        ), buyer=self.create_buyer_B102(), products=[self.create_product_P702(8)])
        bill_B103 = Bill(bill_id="FX103", sale_date=date.today(), seller=self.create_seller_S502(
        ), buyer=self.create_buyer_B102(), products=[self.create_product_P703(1000), self.create_product_P702(800)])
        bill_B104 = Bill(bill_id="FX104", sale_date=date.today(), seller=self.create_seller_S503(
        ), buyer=self.create_buyer_B103(), products=[self.create_product_P703(28), self.create_product_P705(8)])
        bill_B105 = Bill(bill_id="FX105", sale_date=date.today(), seller=self.create_seller_S503(
        ), buyer=self.create_buyer_B103(), products=[self.create_product_P704(7), self.create_product_P706(2)])
        bill_B106 = Bill(bill_id="FX106", sale_date=date.today(), seller=self.create_seller_S504(
        ), buyer=self.create_buyer_B101(), products=[self.create_product_P704(1), self.create_product_P701(1)])
        bill_B107 = Bill(bill_id="FX107", sale_date=date.today(), seller=self.create_seller_S504(
        ), buyer=self.create_buyer_B102(), products=[self.create_product_P704(13), self.create_product_P703(3)])
        bill_B108 = Bill(bill_id="FX108", sale_date=date.today(), seller=self.create_seller_S504(
        ), buyer=self.create_buyer_B103(), products=[self.create_product_P704(10)])
        bill_B109 = Bill(bill_id="FX109", sale_date=date.today(), seller=self.create_seller_S504(
        ), buyer=self.create_buyer_B103(), products=[self.create_product_P704(50)])
        bill_B110 = Bill(bill_id="FX110", sale_date=date.today(), seller=self.create_seller_S504(
        ), buyer=self.create_buyer_B103(), products=[self.create_product_P704(11)])
        bill_B111 = Bill(bill_id="FX111", sale_date=date.today(), seller=self.create_seller_S501(
        ), buyer=self.create_buyer_B102(), products=[self.create_product_P701(25)])
        list_bills.append(bill_B101)
        list_bills.append(bill_B102)
        list_bills.append(bill_B103)
        list_bills.append(bill_B104)
        list_bills.append(bill_B105)
        list_bills.append(bill_B106)
        list_bills.append(bill_B107)
        list_bills.append(bill_B108)
        list_bills.append(bill_B109)
        list_bills.append(bill_B110)
        list_bills.append(bill_B111)

        return list_bills

    def create_bills_example(self):
        """Create a bill multiple items and buyers
        """
        list_bills = []
        bill_B101 = Bill(bill_id="FX101", sale_date=date.today(), seller=self.create_seller_S501(
        ), buyer=self.create_buyer_B101(), products=[self.create_product_P701(15)])
        bill_B102 = Bill(bill_id="FX102", sale_date=date.today(), seller=self.create_seller_S501(
        ), buyer=self.create_buyer_B102(), products=[self.create_product_P702(80)])
        bill_B103 = Bill(bill_id="FX103", sale_date=date.today(), seller=self.create_seller_S502(
        ), buyer=self.create_buyer_B103(), products=[self.create_product_P703(14), self.create_product_P702(20)])

        list_bills.append(bill_B101)
        list_bills.append(bill_B102)
        list_bills.append(bill_B103)

        return list_bills

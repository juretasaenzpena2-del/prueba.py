from __future__ import annotations
from abc import ABC, abstractmethod


class Person(ABC):
    """
    Clase abstracta base para Buyer y Seller.
    Atributos comunes identificados: dni, email, mobile.
    """

    def __init__(self, dni: str, email: str, mobile: str) -> None:
        self.dni = dni
        self.email = email
        self.mobile = mobile

    @abstractmethod
    def print(self) -> None:
        """Imprime la información de la entidad."""
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(dni={self.dni!r})"


class Buyer(Person):
    def __init__(
        self,
        dni: str,
        full_name: str,
        age: int,
        email: str,
        mobile: str,
        address: str
    ) -> None:
        super().__init__(dni=dni, email=email, mobile=mobile)
        self.full_name = full_name
        self.age = age
        self.address = address

    def print(self) -> None:
        print(
            f"Buyer(dni={self.dni}, full_name={self.full_name}, age={self.age}, "
            f"email={self.email}, mobile={self.mobile}, address={self.address})"
        )


class Seller(Person):
    def __init__(
        self,
        dni: str,
        email: str,
        mobile: str,
        bussines_name: str,
        bussines_address: str
    ) -> None:
        super().__init__(dni=dni, email=email, mobile=mobile)
        self.bussines_name = bussines_name
        self.bussines_address = bussines_address

    def print(self) -> None:
        print(
            f"Seller(dni={self.dni}, email={self.email}, mobile={self.mobile}, "
            f"bussines_name={self.bussines_name}, bussines_address={self.bussines_address})"
        )

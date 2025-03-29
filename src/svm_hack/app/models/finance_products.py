from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
import json


class RiskLevel(str, Enum):
    LOW = "niskie"
    MEDIUM = "średnie"
    HIGH = "wysokie"


class ProductType(str, Enum):
    BOND = "obligacja"
    STOCK = "akcja"
    FUND = "fundusz_inwestycyjny"
    ETF = "etf"
    DEPOSIT = "depozyt"
    CRYPTOCURRENCY = "kryptowaluta"
    REAL_ESTATE = "nieruchomość"
    GOLD = "złoto"
    IKE = "ike"
    IKZE = "ikze"


class ProductParameters(BaseModel):
    min_reutrn: float = 0.0
    max_return: float = 0.0

    class Config:
        extra = "allow"  # Pozwala na dodatkowe parametry nieujęte w modelu


class FinancialProduct(BaseModel):
    name: str = Field(..., min_length=1, description="Nazwa produktu finansowego")
    type: ProductType = Field(..., description="Typ produktu finansowego")
    risk: RiskLevel = Field(..., description="Poziom ryzyka związanego z produktem")
    parameters: ProductParameters = Field(..., description="")
    description: Optional[str] = Field("", description="Szczegółowy opis produktu")

    class Config:
        schema_extra = {
            "example": {
                "name": "Obligacje Skarbowe",
                "id"
                "type": "obligacja",
                "risk": "niskie",
                "description": "Dłużne papiery wartościowe emitowane przez Skarb Państwa.",
            }
        }


class FinancialProductDatabase(BaseModel):
    products: List[FinancialProduct] = Field(default_factory=list)

    def add_product(self, product: FinancialProduct):
        self.products.append(product)

    def find_by_risk(self, risk: RiskLevel) -> List[FinancialProduct]:
        return [p for p in self.products if p.risk == risk]

    def find_by_type(self, type: ProductType) -> List[FinancialProduct]:
        return [p for p in self.products if p.type == type]

    def to_json(self) -> str:
        return json.dumps(
            [p.model_dump_json() for p in self.products], ensure_ascii=False, indent=2
        )

    def save_to_file(self, path: str = "financial_products.json"):
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_json())

    def load_from_file(self, path: str = "financial_products.json"):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.products = [FinancialProduct(**item) for item in data]


product_database = FinancialProductDatabase()


# Dodawanie produktów
product_database.add_product(
    FinancialProduct(
        name="Obligacje Skarbowe",
        type=ProductType.BOND,
        risk=RiskLevel.LOW,
        description="Dłużne papiery wartościowe emitowane przez Skarb Państwa. Obligacje skarbowe są instrumentem finansowym o stałym oprocentowaniu, oferującym regularne wypłaty odsetek. Cechują się niskim poziomem ryzyka, gdyż są gwarantowane przez państwo. Obligacje mają określony termin wykupu, zwykle od 2 do 10 lat. Sprawdzają się jako podstawa bezpiecznego portfela inwestycyjnego lub element dywersyfikacji przy bardziej ryzykownych inwestycjach. Dostępne są dla inwestorów indywidualnych poprzez banki i domy maklerskie. Oprocentowanie zazwyczaj wynosi 2,5-4,5% rocznie, a minimalna kwota inwestycji to 100 zł. Charakteryzują się średnią płynnością, ale niską dywersyfikacją.",
        parameters=ProductParameters(min_return=0.03, max_return=0.06),
    )
)

product_database.add_product(
    FinancialProduct(
        name="Złoto",
        type=ProductType.GOLD,
        risk=RiskLevel.LOW,
        description="Metal szlachetny uznawany za bezpieczną przystań inwestycyjną w okresach niepewności gospodarczej. Złoto jest tradycyjnym środkiem przechowywania wartości, szczególnie w czasach inflacji i kryzysów finansowych. Można w nie inwestować na różne sposoby, w tym poprzez zakup fizycznego kruszcu (sztabki, monety), ETF-y oparte na złocie, akcje spółek wydobywczych czy kontrakty terminowe. Cena złota podlega wahaniom, ale historycznie wykazuje tendencję wzrostową w długim terminie. Złoto nie generuje odsetek ani dywidend, jego wartość wynika wyłącznie ze zmiany ceny rynkowej. Charakteryzuje się średnią zmiennością, wysoką płynnością i średnim poziomem dywersyfikacji. Minimalna inwestycja to około 500 zł.",
        parameters=ProductParameters(min_return=-0.1, max_return=0.12),
    )
)

product_database.add_product(
    FinancialProduct(
        name="Akcje",
        type=ProductType.STOCK,
        risk=RiskLevel.HIGH,
        description="Akcje to udziały w spółkach notowanych na giełdach papierów wartościowych. Inwestowanie w akcje pozwala na udział w zyskach firm, zarówno przez wzrost wartości akcji, jak i dywidendy. Charakteryzują się wysoką zmiennością i płynnością, co umożliwia szybki handel. Inwestycja w akcje wiąże się z ryzykiem, ponieważ ich wartość może się zmieniać w zależności od wyników spółek i warunków rynkowych. Zalecana minimalna inwestycja to około 1000 zł.",
        parameters=ProductParameters(min_return=-0.2, max_return=0.25),
    )
)


product_database.add_product(
    FinancialProduct(
        name="Lokata Bankowa",
        type=ProductType.DEPOSIT,
        risk=RiskLevel.LOW,
        description="Depozyt bankowy o stałym oprocentowaniu i gwarantowanym zwrocie kapitału. Lokaty bankowe są jednym z najbezpieczniejszych instrumentów finansowych, gwarantowanym przez Bankowy Fundusz Gwarancyjny do równowartości 100 000 euro. Oferują ustalone z góry oprocentowanie na określony czas, zwykle od 1 miesiąca do 3 lat. Wcześniejsze wycofanie środków może wiązać się z utratą odsetek. Oprocentowanie lokat jest zwykle niższe niż potencjalne zyski z bardziej ryzykownych inwestycji, ale w okresach wysokich stóp procentowych może stanowić atrakcyjną alternatywę. Lokaty są idealne jako element bezpiecznej części portfela inwestycyjnego lub rozwiązanie dla osób unikających ryzyka. Oprocentowanie waha się zazwyczaj w granicach 2-6% rocznie, a minimalny wkład to około 1000 zł. Cechują się niską płynnością ze względu na kary za wcześniejsze wycofanie środków.",
        parameters=ProductParameters(min_return=0.03, max_return=0.05),
    )
)

product_database.add_product(
    FinancialProduct(
        name="Nieruchomości",
        type=ProductType.REAL_ESTATE,
        risk=RiskLevel.LOW,
        description="Nieruchomości to jedna z najbezpieczniejszych form inwestycji, charakteryzująca się stabilnym wzrostem wartości w długim okresie. Inwestowanie w nieruchomości może obejmować zakup mieszkań, domów, lokali użytkowych czy gruntów, zarówno w celach mieszkaniowych, jak i komercyjnych. Dzięki niskiemu poziomowi ryzyka i potencjalnym dochodom pasywnym z wynajmu, jest to atrakcyjna opcja dla inwestorów poszukujących stabilności i ochrony kapitału przed inflacją.",
        parameters=ProductParameters(min_return=-0.05, max_return=0.14),
    )
)

product_database.add_product(
    FinancialProduct(
        name="Kryptowaluty",
        type=ProductType.CRYPTOCURRENCY,
        risk=RiskLevel.HIGH,
        description="Kryptowaluty to cyfrowe aktywa oparte na technologii blockchain, które umożliwiają szybkie i zdecentralizowane transakcje. Charakteryzują się wysoką zmiennością cen i spekulacyjnym charakterem, co wiąże się zarówno z możliwością osiągnięcia wysokich zysków, jak i znaczących strat. Inwestowanie w kryptowaluty wymaga dobrej znajomości rynku oraz akceptacji wysokiego poziomu ryzyka. Popularne kryptowaluty to m.in. Bitcoin, Ethereum i inne altcoiny, które mogą być używane zarówno jako środek płatniczy, jak i forma długoterminowej inwestycji.",
        parameters=ProductParameters(min_return=-0.4, max_return=0.4),
    )
)

product_database.add_product(
    FinancialProduct(
        name="ETF",
        type=ProductType.ETF,
        risk=RiskLevel.MEDIUM,
        description="ETF (Exchange Traded Fund) to fundusz inwestycyjny notowany na giełdzie, który umożliwia inwestorom łatwy dostęp do zdywersyfikowanego portfela aktywów. ETF-y mogą obejmować akcje, obligacje, surowce lub inne instrumenty finansowe, śledząc określone indeksy lub strategie inwestycyjne. Dzięki swojej strukturze oferują niższe koszty zarządzania w porównaniu do tradycyjnych funduszy inwestycyjnych oraz możliwość kupna i sprzedaży jednostek w czasie rzeczywistym na giełdzie. Są atrakcyjnym rozwiązaniem dla inwestorów poszukujących równowagi między ryzykiem a potencjalnym zwrotem.",
        parameters=ProductParameters(min_return=0.02, max_return=0.1),
    )
)

product_database.add_product(
    FinancialProduct(
        name="IKE i IKZE",
        type=ProductType.IKE,  # Możesz użyć IKE jako reprezentacji obu typów
        risk=RiskLevel.LOW,
        description="IKE (Indywidualne Konto Emerytalne) oraz IKZE (Indywidualne Konto Zabezpieczenia Emerytalnego) to produkty do oszczędzania na emeryturę z korzyściami podatkowymi. IKE umożliwia zwolnienie z podatku od zysków kapitałowych, natomiast IKZE pozwala na odliczenie wpłat od podstawy opodatkowania. Oba produkty oferują inwestycje w lokaty, fundusze, obligacje czy akcje, stanowiąc bezpieczne rozwiązanie dla osób planujących przyszłość finansową.",
        parameters=ProductParameters(min_return=0.04, max_return=0.11),
    )
)

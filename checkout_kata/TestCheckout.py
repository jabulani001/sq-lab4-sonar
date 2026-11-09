import pytest
from Checkout import Checkout


@pytest.fixture()
def checkout():
    checkout = Checkout()
    checkout.addItemPrice("a", 1)
    checkout.addItemPrice("b", 2)
    return checkout

def test_CanCalculateTotal(checkout):
    checkout.addItem("a")
    assert checkout.calculateTotal() == 1

def test_GetCorrectTotalWithMultipleItems(checkout):
    checkout.addItem("a")
    checkout.addItem("b")
    assert checkout.calculateTotal() == 3

def test_canAddDiscountRule(checkout):
    checkout.addDiscount("a", 3, 2)

def test_canApplyDiscountRule(checkout):
    checkout.addDiscount("a", 3, 2)
    checkout.addItem("a")
    checkout.addItem("a")
    checkout.addItem("a")
    assert checkout.calculateTotal() == 2

def test_ExceptionWithBadItem(checkout):
    with pytest.raises(Exception):
        checkout.addItem("c")


# Part B: eigene Testfälle

# Leerer Warenkorb muss 0 kosten
def test_emptyCartTotalIsZero(checkout):
    assert checkout.calculateTotal() == 0

# Rabatt plus Rest: 3 Stück im Angebot, das 4. zum normalen Preis (hat den / Fehler gefunden)
def test_canApplyDiscountRuleWithRemainder(checkout):
    # 4x "a", Rabatt 3 für 2  ->  2 (Rabatt) + 1 (Rest) = 3
    checkout.addDiscount("a", 3, 2)
    for _ in range(4):
        checkout.addItem("a")
    assert checkout.calculateTotal() == 3

# Rabatt greift mehrmals: 7 Stück = 2x Angebot + 1 normal
def test_canApplyDiscountRuleMultipleTimes(checkout):
    # 7x "a", Rabatt 3 für 2  ->  2 + 2 + 1 = 5
    checkout.addDiscount("a", 3, 2)
    for _ in range(7):
        checkout.addItem("a")
    assert checkout.calculateTotal() == 5

# Negativer Preis ist verboten und muss einen Fehler werfen
def test_negativePriceRaisesException(checkout):
    with pytest.raises(ValueError):
        checkout.addItemPrice("x", -1)

# Lab 3 Part B: Rabatt existiert, aber zu wenige Stück gekauft -> normaler Preis (deckt die rote Zeile 46 ab)
def test_discountNotAppliedWithTooFewItems(checkout):
    # 2x "a", Rabatt erst ab 3 Stück  ->  2 x 1 = 2
    checkout.addDiscount("a", 3, 2)
    checkout.addItem("a")
    checkout.addItem("a")
    assert checkout.calculateTotal() == 2

# Lab 4: Gutscheincodes
def test_couponCodeHasRequestedLength(checkout):
    assert len(checkout.generateCouponCode(12)) == 12

def test_couponCodeUsesOnlyUppercaseAndDigits(checkout):
    code = checkout.generateCouponCode()
    assert code.isalnum() and code == code.upper()

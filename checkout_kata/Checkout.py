import secrets
import string


class Checkout:
    class Discount:
        def __init__(self, nbrItems, price):
            self.nbrItems = nbrItems
            self.price = price

    def __init__(self):
        self.prices = {}
        self.discounts = {}
        self.items = {}


    def addDiscount(self, item, nbrOfItems, price):
        discount = self.Discount(nbrOfItems, price)
        self.discounts[item] = discount


    def addItemPrice(self, item, price):
        if price < 0:
            raise ValueError("Negative price")
        self.prices[item] = price

    def addItem(self, item):
        if item not in self.prices:
            raise Exception("Bad Item")

        if item in self.items:
            self.items[item] += 1
        else:
            self.items[item] = 1

    def calculateTotal(self):
        total = 0
        for item, cnt in self.items.items():
            total += self.calculateItemTotal(item, cnt)
        return total

    def calculateItemTotal(self, item, cnt):
        total = 0
        if item in self.discounts:
            discount = self.discounts[item]
            if cnt >= discount.nbrItems:
                total += self.calculateItemDiscountedTotal(item, cnt, discount)
            else:
                total += self.prices[item] * cnt
        else:
            total += self.prices[item] * cnt

        return total

    def calculateItemDiscountedTotal(self, item, cnt, discount):
        total = 0
        nbrOfDiscounts = cnt // discount.nbrItems  #hier war der Fehler dass es nur ein / war und nicht //
        total += nbrOfDiscounts * discount.price
        remaining = cnt % discount.nbrItems
        total += remaining * self.prices[item]
        return total

    def generateCouponCode(self, length=8):
        alphabet = string.ascii_uppercase + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(length))

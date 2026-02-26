# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
Task 'Tangled Reef' — THE MESS

This code works. It prints correct results. It is also a masterclass in how
NOT to write software. Every SOLID principle is violated at least once.

Your job: understand what it does, identify the violations, then refactor it.
Do NOT change the output — only the structure.
"""


class App:
    """Does everything. Knows everything. Fears nothing. Maintains nothing."""

    def __init__(self):
        self.items = []
        self.tax = 0.19
        self.discount_codes = {"SAVE10": 0.10, "HALF": 0.50, "VIP": 0.25}
        self.log = []

    def add(self, name, price, qty, category):
        self.items.append({"name": name, "price": price, "qty": qty, "cat": category})

    def calc(self, code=None):
        total = 0
        receipt_lines = []
        for item in self.items:
            line_total = item["price"] * item["qty"]

            # category-specific tax override — because why not hardcode it
            if item["cat"] == "food":
                tax_rate = 0.07
            elif item["cat"] == "luxury":
                tax_rate = 0.25
            else:
                tax_rate = self.tax

            line_with_tax = line_total * (1 + tax_rate)
            total += line_with_tax

            # formatting is also this method's job, obviously
            receipt_lines.append(
                f"  {item['name']:20s} {item['qty']:3d} x {item['price']:8.2f} "
                f"= {line_with_tax:10.2f} (tax {tax_rate:.0%})"
            )

            # logging too — we're a full-stack method
            self.log.append(f"Processed: {item['name']}")

        # discount handling — right here in the calculation
        discount = 0
        if code and code in self.discount_codes:
            discount = total * self.discount_codes[code]
            total -= discount
            receipt_lines.append(f"  {'Discount (' + code + ')':20s}             = {-discount:10.2f}")
            self.log.append(f"Applied discount: {code}")
        elif code:
            receipt_lines.append(f"  ** Invalid code: {code} **")
            self.log.append(f"Invalid code attempted: {code}")

        # report generation — because one method should do at least 5 things
        receipt_lines.insert(0, "=" * 58)
        receipt_lines.insert(1, f"  {'RECEIPT':^54s}")
        receipt_lines.insert(2, "=" * 58)
        receipt_lines.append("-" * 58)
        receipt_lines.append(f"  {'TOTAL':20s}             = {total:10.2f}")
        receipt_lines.append("=" * 58)

        # also writes to file — because why separate concerns
        with open("receipt.txt", "w") as f:
            for line in receipt_lines:
                f.write(line + "\n")
        self.log.append("Receipt written to receipt.txt")

        return total, receipt_lines

    def print_receipt(self, code=None):
        total, lines = self.calc(code)
        for line in lines:
            print(line)
        print()
        return total

    def print_log(self):
        print("--- Log ---")
        for entry in self.log:
            print(f"  [{entry}]")

    def export_csv(self):
        # CSV export — also this class's responsibility
        with open("items.csv", "w") as f:
            f.write("name,price,qty,category,line_total\n")
            for item in self.items:
                lt = item["price"] * item["qty"]
                f.write(f"{item['name']},{item['price']},{item['qty']},{item['cat']},{lt}\n")
        self.log.append("CSV exported to items.csv")

    def stats(self):
        # analytics — why not, we're already here
        if not self.items:
            print("No items.")
            return
        prices = [i["price"] * i["qty"] for i in self.items]
        avg = sum(prices) / len(prices)
        most_expensive = max(self.items, key=lambda i: i["price"] * i["qty"])
        cheapest = min(self.items, key=lambda i: i["price"] * i["qty"])
        print(f"  Items:          {len(self.items)}")
        print(f"  Avg line total: {avg:.2f}")
        print(f"  Most expensive: {most_expensive['name']} ({most_expensive['price'] * most_expensive['qty']:.2f})")
        print(f"  Cheapest:       {cheapest['name']} ({cheapest['price'] * cheapest['qty']:.2f})")

    # bonus: a method that changes behavior based on a string flag
    def do(self, action, **kwargs):
        if action == "receipt":
            return self.print_receipt(kwargs.get("code"))
        elif action == "csv":
            self.export_csv()
        elif action == "stats":
            self.stats()
        elif action == "log":
            self.print_log()
        else:
            print(f"Unknown action: {action}")


if __name__ == "__main__":
    app = App()
    app.add("Organic Bread", 3.49, 2, "food")
    app.add("Gold-leaf Chocolate", 29.99, 1, "luxury")
    app.add("USB Cable", 7.95, 3, "electronics")
    app.add("Vintage Wine", 45.00, 1, "luxury")
    app.add("Rice (5kg)", 8.99, 1, "food")

    app.do("receipt", code="SAVE10")
    app.do("stats")
    app.do("csv")
    app.do("log")

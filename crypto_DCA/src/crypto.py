class Mycrypto:
    def __init__(self,symbol,cost,amount,date):
        self.name = symbol
        self.cost = cost
        self.amount = amount
        self.date = date
        self.avg_price = cost/amount

    def __str__(self):
        return self.name + self.cost
    

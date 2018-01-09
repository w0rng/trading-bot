class Currency():
	def __init__(self, symbol, ask, bid, rank, quantityIncrement, quantity = 0):
		self.symbol = symbol
		self.ask = ask
		self.bid = bid
		self.rank = rank
		self. quantity = quantity
		self.quantityIncrement = quantityIncrement
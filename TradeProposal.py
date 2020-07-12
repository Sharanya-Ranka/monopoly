#import Player

class TradeProposal():
	def __init__(self,trader,tradee):
		self.trader=trader
		self.tradee=tradee
		self.requested_properties=[]
		self.togive_properties=[]
		self.requested_money=0
		self.togive_money=0


	def request_properties_and_money(self):##Last element has money requested
		requested_properties_money=self.trader.request_properties_and_money(self.tradee)
		self.requested_properties=requested_properties_money[:-1]
		self.requested_money=requested_properties_money[-1]

	def togive_properties_and_money(self):##Last element has money togive
		togive_properties_money=self.trader.togive_properties_and_money(self.tradee)
		self.togive_properties=togive_properties_money[:-1]
		self.togive_money=togive_properties_money[-1]

	def present_trade(self):
		if self.requested_money>self.togive_money:
			self.requested_money-=self.togive_money
			self.togive_money=0
		if self.togive_money>self.requested_money:
			self.togive_money-=self.requested_money
			self.requested_money=0
		agreed_status=self.tradee.present_trade(self.trader,self.requested_properties,self.togive_properties,self.requested_money,self.togive_money)	##Boolean value returned
		if agreed_status==True:
			
			for req_prop in self.requested_properties:
				print(self.trader.name,"has got",req_prop.name,"from",self.tradee.name)
				req_prop.owner=self.trader
				self.tradee.asset_list.remove(req_prop)
				self.trader.asset_list.append(req_prop)

			for give_prop in self.togive_properties:
				print(self.trader.name,"has given",give_prop.name,"to",self.tradee.name)
				give_prop.owner=self.tradee
				self.trader.asset_list.remove(give_prop)
				self.tradee.asset_list.append(give_prop)

			if self.requested_money!=0:
				print(self.trader.name,"has got Rs",self.requested_money,"from",self.tradee.name)
			if self.togive_money!=0:
				print(self.trader.name,"has given Rs",self.togive_money,"to",self.tradee.name)
			self.tradee.cash+=self.togive_money-self.requested_money
			self.trader.cash+=self.requested_money-self.togive_money

			print("Trade between ",self.trader.name," and ",self.tradee.name," successful.")
		else:
			print("Trade between ",self.trader.name," and ",self.tradee.name," unsuccessful.")


# p1=Player.Human("Player1")
# p2=Player.Human("Player2")
# p1.diceval=1
# p2.diceval=3
# p1.update_position()
# p2.update_position()
# tp=TradeProposal(p1,p2)
# tp.request_properties_and_money()
# tp.togive_properties_and_money()
# tp.present_trade()

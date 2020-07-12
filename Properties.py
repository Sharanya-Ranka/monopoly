class Properties():
	def __init__(self,name,price,colour,position,owner,titledeed,property_type):
		self.name=name
		self.price=price
		self.colour=colour
		self.position=position    #position is counted from 0(GO) to 39(Mayfair)
		self.owner=owner          ##owner should be of type Player
		self.titledeed=titledeed  #form is[no houses,1house,2houses,3houses,4houses,hotel]
		self.mortgage_val=self.price//2
		self.mortgaged_status=0    ##1 for mortgaged, 0 for redeemed/normal
		self.type=property_type
		

	def get_name(self):
		return(self.name)

	def get_price(self):
		return(self.price)

	def get_colour(self):
		return(self.colour)

	def get_position(self):
		return(self.position)

	def get_owner(self):
		return(self.owner)

	def get_titledeed(self):
		return(self.titledeed)

	def get_mortgage_val(self):
		return(self.mortgage_val)

	def set_owner(self,new_owner):
		self.owner=new_owner    ##New owner of type Player

	def set_mortgaged_status(self,status):
		self.mortgaged_status=status

	def trade_property(self,tradee):       ##Tradee is new_owner of type Player
		if(self.hotels+self.houses!=0):
			return(0)                     ##Error code 0: there must be no houses or hotels to trade
		else:
			self.set_owner(tradee)
			return(1)                    ##Success

	def get_value(self):                     ##Get current value of the property
		if(self.mortgaged_status==1):
			return(self.mortgage_val)
		else:
			return(self.price)

	def mortgage_property(self):                      
		if(self.mortgaged_status==1):
			return(0)                         ##Error code 0: Property already mortgaged
		else:
			self.set_mortgaged_status(1)
			return(1)

	def redeem_property(self):
		if(self.mortgaged_status==0):
			return(0)                         ##Error code 0: Property already redeemed
		else:
			self.set_mortgaged_status(0)
			return(1)




class Residence(Properties):
	def __init__(self,name,price,colour,position,owner,titledeed):
		Properties.__init__(self,name,price,colour,position,owner,titledeed,"Residence")
		self.houses=0
		self.hotels=0

	def get_houses(self):
		return(self.houses)

	def get_hotels(self):
		return(self.hotels)

	def houseval(self):
		return(50*((self.position//10)+1))

	def change_no_buildings(self,build_type,no):       ##To change the number of houses or hotels on property
		if build_type=="houses":
			if no+self.houses>4 or no+self.houses<0:
				return(False)
			else:
				self.houses+=no
				return(True)

		elif build_type=="hotels":
			if no+self.hotels>1 or no+self.hotels<0:
				return(False)
			else:
				self.hotels+=no
				return(True)

		else:
			return(False)

	def get_rent(self,multiplier):                           ##To get rent on landing on property
		if self.mortgaged_status==1:
			return(0)
		else:
			return(self.titledeed[self.houses+self.hotels]*multiplier)

	def get_value(self):                     ##Get current value of the property  Overrides Property function
		if(self.mortgaged_status==1):
			return(self.mortgage_val)
		else:
			return(self.price+(self.houses+self.hotels)*self.houseval())

	def mortgage_property(self):				## Overrides property function
		if(self.houses+self.hotels>0):
			return(-1)                        ##Error code -1: there must be no houses or hotels to mortgage
		elif(self.mortgaged_status==1):
			return(0)                         ##Error code 0: Property already mortgaged
		else:
			self.set_mortgaged_status(1)
			return(1)

	def show_deed(self):
		print("Price of property= Rs"+str(self.price))
		print("Descr.\t\tRent")
		print("------\t\t----")
		print("Site\t\t"+str(self.titledeed[0]))
		print("1 house\t\t"+str(self.titledeed[1]))
		print("2 houses\t"+str(self.titledeed[2]))
		print("3 houses\t"+str(self.titledeed[3]))
		print("4 houses\t"+str(self.titledeed[4]))
		print("Hotel\t\t"+str(self.titledeed[5]))
		print()




class Utility(Properties):
	def __init__(self,name,price,colour,position,owner,titledeed):
		Properties.__init__(self,name,price,colour,position,owner,titledeed,"Utility")

	def get_rent(self,dice_val,no_of_utilities):                           ##To get rent on landing on property
		if self.mortgaged_status==1:
			return(0)
		elif(no_of_utilities==1):
			return(4*dice_val)
		elif(no_of_utilities==2):
			return(10*dice_val)
		else:
			return(0)

	def show_deed(self):
		print("Price of property= Rs"+str(self.price))
		print("Descr.\t\tRent")
		print("------\t\t----")
		print("1 utility\t\t4*dice value")
		print("1 utilities\t\t10*dice value")
		print()




class Station(Properties):
	def __init__(self,name,price,colour,position,owner,titledeed):
		Properties.__init__(self,name,price,colour,position,owner,titledeed,"Station")

	def get_rent(self,no_of_stations):
		if no_of_stations>=1:
			return(25*pow(2,no_of_stations-1))
		else:
			return(0)

	def show_deed(self):
		print("Price of property= Rs"+str(self.price))
		print("Descr.\t\tRent")
		print("------\t\t----")
		#print("Site\t"+str(self.titledeed[0]))
		print("1 station\t"+str(25))
		print("2 stations\t"+str(50))
		print("3 stations\t"+str(100))
		print("4 stations\t"+str(200))
		#print("Hotel\t"+str(self.titledeed[6]))
		print()



class Others():
	def __init__(self,name,position,ptype):
		self.name=name
		self.position=position
		self.type=ptype









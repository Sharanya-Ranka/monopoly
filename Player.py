import random
import Properties
#import GameBoard                        ##GameBoard is a class to get everything together. We will use its static variables here
import Cards
import Tiles
import PlayerInteraction




class Player():
        ## Class player is one of the most important classes in monopoly.
        ## There will be 2 child classes- Machine and Human.
        ## It will act as a common "interface" for two types of players
        ## Human class will contain methods to input/output data to the console(monitor)
        ## Machine class will contain methods to make decisions in the game(Logic for playing game)
        ## Player class will do most of the internal handling of operations once input is got/decision is made.
        ## Objects will be made of Human and Machine subclasses only, so the methods in this class can be named without much thought.
        def __init__(self,name,player_type):
                self.name=name
                self.cash=1500
                self.asset_list=[]                      ## A list of properties of type Properties
                self.position=0
                self.jailfreecard=[]
                self.injail=0                   ## injail determines if player is in jail and if yes, for how many turns(3-just jailed,2-after 1 move,1-after 2 moves)
                self.type=player_type
                self.diceval=0
                #self.tiles=GameBoard.tiles                     ##Tile list will contain objects of Properties and OtherTiles classes(0 to 39)

        def get_mortgageable_assets(self):
                mortgageable_assets=[]
                for asset in self.asset_list:
                        if asset.mortgaged_status==0 and (asset.type!="Residence" or asset.get_houses()+asset.get_hotels()==0):
                                mortgageable_assets.append(asset)
                return(mortgageable_assets)

        def mortgage_on_these(self,mortgageable_assets,mortgage_on):
                for ind in mortgage_on:
                        asset=mortgageable_assets[ind-1]
                        check=asset.mortgage_property()
                        if check==0:                                                                    ## Redundant as get_mortgageable_assets already checks for this
                                print(asset.name,"is already mortgaged")
                        elif check==-1:                                                                   ## Redundant as get_mortgageable_assets already checks for this
                                print("Houses and/or hotels exist on property. Cannot mortgage",asset.name)
                        elif check==1:
                                print(self.name,"mortgaged",asset.name)
                                self.cash+=asset.get_mortgage_val()

        def get_redeemable_assets(self):
                redeemable_assets=[]
                for asset in self.asset_list:
                        if asset.mortgaged_status==1:
                                redeemable_assets.append(asset)
                return(redeemable_assets)

        def redeem_on_these(self,redeemable_assets,redeem_on):
                for ind in redeem_on:
                        asset=redeemable_assets[ind-1]
                        if self.cash>=int(asset.get_mortgage_val()*1.1):
                                check=asset.redeem_property()
                                if check==0:                                                            ## Redundant as get_redeemable_assets already checks for this
                                        print(asset.name,"is already redeemed")
                                elif check==1:
                                        print(self.name,"redeemed",asset.name)
                                        self.cash-=int(asset.get_mortgage_val()*1.1)
                        else:                                                                                   ## Machine class should check for this beforehand. This should not occur for machine object
                                print("Insufficient funds to redeem",asset.name)

        def get_buildable_assets(self):
                asset_dict={}
                buildable_assets=[]
                for asset in self.asset_list:
                        if asset.type=="Residence":
                                if asset.colour not in asset_dict:
                                        asset_dict[asset.colour]=[5,[]]               ##no. 1 is minimum no. of houses+hotels list2 is assets
                                asset_dict[asset.colour][1].append(asset)
                                if asset.get_houses()+asset.get_hotels()<asset_dict[asset.colour][0]:
                                        asset_dict[asset.colour][0]=asset.get_houses()+asset.get_hotels()

                for colour in asset_dict:
                        if colour.lower()!="brown" and colour.lower()!="dark blue" and len(asset_dict[colour][1])==3:
                                asset_list=asset_dict[colour][1]
                                for asset in asset_list:
                                        if asset.get_houses()+asset.get_hotels()==asset_dict[colour][0] and asset.get_houses()+asset.get_hotels()<5 and asset.mortgaged_status==0:
                                                buildable_assets.append(asset)

                        elif (colour.lower()=="brown" or colour.lower()=="dark blue") and len(asset_dict[colour][1])==2:
                                asset_list=asset_dict[colour][1]
                                for asset in asset_list:
                                        if asset.get_houses()+asset.get_hotels()==asset_dict[colour][0] and asset.get_houses()+asset.get_hotels()<5 and asset.mortgaged_status==0:
                                                buildable_assets.append(asset)

                return(buildable_assets)

        def build_on_these(self,buildable_assets,build_on):
                for ind in build_on:
                        asset=buildable_assets[ind-1]
                        if self.cash>=asset.houseval():
                                self.cash-=asset.houseval()
                                b=False
                                if asset.get_houses()<4:
                                        b=asset.change_no_buildings("houses",1)
                                else:
                                        b=asset.change_no_buildings("hotels",1)
                                if b==False:
                                    print("House/hotel build failed")
                        else:
                                print("Insufficient funds to build on",asset.name)


        def get_sellable_assets(self):
                asset_dict={}
                sellable_assets=[]
                for asset in self.asset_list:
                        if asset.type=="Residence":
                                if asset.colour not in asset_dict:
                                        asset_dict[asset.colour]=[0,[]]               ##List 1 is maximum no. of houses+hotels list2 is assets
                                asset_dict[asset.colour][1].append(asset)
                                if asset.get_houses()+asset.get_hotels()>asset_dict[asset.colour][0]:
                                        asset_dict[asset.colour][0]=asset.get_houses()+asset.get_hotels()

                for colour in asset_dict:
                        if colour.lower()!="brown" and colour.lower()!="dark blue" and len(asset_dict[colour][1])==3:
                                asset_list=asset_dict[colour][1]
                                for asset in asset_list:
                                        if asset.get_houses()+asset.get_hotels()==asset_dict[colour][0] and asset.get_houses()+asset.get_hotels()>0:
                                                sellable_assets.append(asset)

                        elif (colour.lower()=="brown" or colour.lower()=="dark blue") and len(asset_dict[colour][1])==2:
                                asset_list=asset_dict[colour][1]
                                for asset in asset_list:
                                        if asset.get_houses()+asset.get_hotels()==asset_dict[colour][0] and asset.get_houses()+asset.get_hotels()>0:
                                                sellable_assets.append(asset)

                return(sellable_assets)

        def sell_on_these(self,sellable_assets,sell_on):
                for ind in sell_on:
                        asset=sellable_assets[ind-1]
                        if(asset.get_houses()+asset.get_hotels()>0):
                                self.cash+=asset.houseval()//2
                                if asset.get_hotels()==1:
                                        asset.change_no_buildings("hotels",-1)
                                elif asset.get_hotels()==0 and asset.get_houses()>0:
                                        asset.change_no_buildings("houses",-1)
                                else:
                                    print("House/hotel sale failed","hotels=",asset.hotels,"houses=",asset.houses)
                        else:
                                print("All buildings already sold",asset.name)

        def get_tradable_assets(self):
                tradable_assets=[]
                for asset in self.asset_list:
                        if asset.type!="Residence" or asset.houses+asset.hotels==0:
                                tradable_assets.append(asset)
                return(tradable_assets)



        def update_position(self):              ## The static variable GameBoard.tile_list is never changed here
                
                self.position=self.position+self.diceval

                if self.position>39:
                        self.position=self.position%40
                        print(self.name,"has passed GO, received Rs 200")
                        self.cash+=200

                tile_landed_on=Tiles.Tiles.tiles[self.position]            ##Each object in tile will have name and type instance variable

                if self.position!=0:
                        print(self.name,"has landed on",tile_landed_on.name)

                if tile_landed_on.type=="Residence" or tile_landed_on.type=="Utility" or tile_landed_on.type=="Station":
                        self.landed_on_property(tile_landed_on)                 ##self and which property landed on passed

                elif tile_landed_on.type=="Community Chest" or tile_landed_on.type=="Chance":
                        self.landed_on_card(tile_landed_on.type)

                elif tile_landed_on.type=="Go to Jail":
                        print(self.name,"is in jail")
                        self.go_to_jail()

                elif tile_landed_on.type=="Income Tax":
                        print("Income Tax taken(Rs200)")
                        self.cash-=200             ##Super Tax and Income Tax tiles will have tax_value instance variables

                elif tile_landed_on.type=="Super Tax":
                        print("Super Tax taken(Rs200)")
                        self.cash-=100             ##Super Tax and Income Tax tiles will have tax_value instance variables


                else:
                        pass
                print()

        def landed_on_property(self,property):
                #print(property.owner)
                if property.owner!="Bank" and property.owner.name!=self.name:                  ##Functionality for paying rent
                        rent=0
                        if property.type=="Residence":
                                multiplier=1
                                if property.get_houses()+property.get_hotels()==0 and property.owner.check_group(property,2,3,4,2):
                                        multiplier=2
                                rent=property.get_rent(multiplier)
                                property.owner.cash+=rent
                                self.cash-=rent

                        elif property.type=="Utility":
                                ##To find no. of unmortgaged utilities
                                utilities=0
                                for prop in property.owner.asset_list:
                                        if prop.type=="Utility" and prop.mortgaged_status==0:
                                                utilities+=1

                                rent=property.get_rent(self.diceval,utilities)
                                property.owner.cash+=rent
                                self.cash-=rent

                        elif property.type=="Station":
                                ##To find number of stations
                                stations=0
                                for prop in property.owner.asset_list:
                                        if prop.type=="Station" and prop.mortgaged_status==0:
                                                stations+=1

                                rent=property.get_rent(stations)
                                property.owner.cash+=rent
                                self.cash-=rent

                        else:
                                pass

                        print(self.name,"payed rent of Rs",rent,"to",property.owner.name)


                elif property.owner!=self:                                                           ##Functionality for buying property
                        property.show_deed()
                        print()
                        c=self.cash
                        tmv=self.total_mortgageable_value()
                        decision="no"
                        if(c>=property.price):
                                decision=self.decide_to_buy(property,1)                 ##Mode number 1= Enough cash

                        elif(c<property.price and c+tmv>=property.price):
                                decision=self.decide_to_buy(property,0)                 ##Mode number 0= Not enough cash but can buy by mortgaging

                        else:
                                PlayerInteraction.PlayerInteraction.auction(property,self)
                                return()

                        if decision=="yes":
                                c=self.cash
                                if(c<property.price):
                                        print("Cash less than property price, ERROR")

                                else:
                                        self.cash-=property.price
                                        property.set_owner(self)
                                        self.asset_list.append(property)
                                        print(self.name,"bought",property.name,"for",property.price)

                        else:
                                PlayerInteraction.PlayerInteraction.auction(property,self)

                

        def landed_on_card(self,card_type):
                Cards.Cards.pickcard(card_type,self)


        def go_to_jail(self):
                self.injail=3
                self.position=10

        def total_mortgageable_value(self):
                value=0
                for asset in self.asset_list:
                        if asset.mortgaged_status==0:
                                value+=asset.get_mortgage_val()
                        if asset.type=="Residence":
                                value+=asset.houseval()*(asset.houses+asset.hotels)
                return(value)

        def isbankrupt(self):
                tmv=self.total_mortgageable_value()
                if(self.cash+tmv>=0):
                        return(False)
                else:
                        return(True)

        def auction_all_properties(self):
                for asset in self.asset_list:
                        if asset.type=="Residence":
                                asset.houses=0
                                asset.hotels=0
                        PlayerInteraction.PlayerInteraction.auction(asset)

        def check_group(self,property,res2,res3,st,ut):
            count=0
            for asset in self.asset_list:
                if asset.colour==property.colour:
                    count+=1
            if (property.colour=="Dark Blue" or property.colour=="Brown") and count==res2:
                return(1)
            elif (property.colour==Tiles.Tiles.tiles[5].colour and count>=st):
                return(1)
            elif (property.colour==Tiles.Tiles.tiles[12].colour and count==ut):
                return(1)
            elif count==res3:
                return(1)
            else:
                return(0)

        @staticmethod
        def validate_int_input(geval,leval,illegal_value_msg="Default"):
            if illegal_value_msg=="Default":
                illegal_value_msg="Illegal value. Input must be integer between "+str(geval)+" and "+str(leval)

            check=True
            while(check):
                i=input()
                if(i.isnumeric() and int(i)>=geval and int(i)<=leval):
                    check=False
                    return(int(i))
                else:
                    print(illegal_value_msg)
                    print("Please input again")
                    print()

        @staticmethod
        def validate_int_array_input(geval,leval,illegal_value_msg="Default"):
            if illegal_value_msg=="Default":
                illegal_value_msg="Illegal value. Input must be (space-separated)integers between "+str(geval)+" and "+str(leval)

            check=True
            while(check):
                flag=0
                i_arr=input().rstrip().split()
                for val in i_arr:
                    if not(val.isnumeric() and int(val)>=geval and int(val)<=leval):
                        flag=1
                        break
                if flag==0:
                    return(list(map(int,i_arr)))
                else:
                    print(illegal_value_msg)
                    print("Please input again")
                    print()


        def show_my_assets(self):
                print(self.name,"'s assets")
                print("Money="+str(self.cash))
                self.show_assets(self.asset_list)
        

        def show_assets(self,asset_list):
                if len(asset_list)!=0:
                    print("Sr.No\tName\t\t\t\tPrice\tMortgaged\tHouses\tHotels")
                    print("-----\t----\t\t\t\t-----\t---------\t------\t------")
                else:
                    print("No properties")

                for i,asset in enumerate(asset_list):
                    spaces=" "*(32-len(asset.name))
                    mortgaged_str="Yes" if asset.mortgaged_status==1 else "No"
                    print(str(i+1)+"\t"+str(asset.name)+spaces+str(asset.price)+"\t"+mortgaged_str+"\t\t",end="")
                    if asset.type=="Residence":
                        print(str(asset.houses)+"\t"+str(asset.hotels))
                    else:
                        print()
                print()





class Human(Player):
        def __init__(self,name):
                Player.__init__(self,name,"Human")

        def make_move(self):
                rolls=0
                print(self.name+"'s money=",self.cash)
                

                print("roll_die(roll) my_assets(ma) all_players'_assets(a) finish_turn(f) build(b) sell(s) mortgage(m) redeem(r) trade(t) exit(e)")

                if self.cash<0 and self.cash+self.total_mortgageable_value()>=0:
                    print("Low on cash, need to mortgage property")
                    self.mortgage()

                elif self.cash<0 and self.cash+self.total_mortgageable_value()<0:
                    print(self.name+"'s have lost the game!!")
                    return()

                if self.injail>0:
                        self.jailoptions()


                b=True
                while(b):
                    print("In moves selection")
                    if self.injail>0:
                        rolls=1

                    command=input()
                    #b=False

                    if command.lower()=="roll" and self.injail==0:
                        if rolls==0:
                                rolls+=1
                                self.roll()
                        else:
                                print("You can only roll once")

                    elif command.lower()=="roll" and self.injail>0:       ##Person is in jail. Do not allow roll
                        print("You are in jail. You cannot roll")
                        rolls=1
                    #     print("You have rolled ",end='') if self.type=="human" else print(self.name,"has rolled ",end='')
                    #     print(die)
                    #     self.pos+=die
                    #     self.pos=self.pos%40
                    #     rolls+=1
                    #     self.perform_action(self.tile[self.pos][0])

                    # elif command.lower()=="roll" and rolls>0 :
                    #     print("only one roll per turn. type f to finish turn.")

                    elif command.lower()=="sr":
                        die=int(input())
                        self.diceval=die
                        self.update_position()

                    elif command.lower()=="ma":
                        self.show_my_assets()            

                    elif command.lower()=="a":
                        PlayerInteraction.PlayerInteraction.show_all_assets()

                    elif command.lower()=="b":
                        self.build()

                    elif command.lower()=="s":
                        self.sell()

                    elif command.lower()=="m":
                        self.mortgage()                 
                        
                    
                    elif command.lower()=="r":
                        self.redeem()              

                    elif command.lower()=="t":
                        PlayerInteraction.PlayerInteraction.trade(self)              
                        

                    elif command.lower()=="e":
                        exit()

                    elif command.lower()=="f" and rolls>0:
                        b=False

                    elif command.lower()=="f" and rolls==0:
                        print("You need to roll the dice!(Type-roll)")

                    else:
                        print("command incorrect, choose one from above")


                       
        def decide_to_buy(self,property,mode):
                print("Do you want to buy '",property.name,"'?(Y/N)")
                if input().lower()=='y':
                        if mode==0:
                                while(self.cash<property.price):
                                        print("Not enough cash. Press 'm' to mortgage and 's' to sell houses/hotels")
                                        while(True):
                                        	ch=input()
                                        	if ch=='m':
                                        		self.mortgage()
                                        		break
                                        	elif ch=='s':
                                        		self.sell()
                                        		break
                                        	else:
                                        		print("Invalid input")

                        if self.cash>=property.price:
                                return("yes")
                        else:
                        		print("Not enough cash to buy(ERROR)")
                        		return("no")

                else:
                        return("no")

        

        def roll(self):
                self.diceval=0
                dice1=0
                dice2=0
                doubles=0
                while(dice1==dice2 and doubles<3):
                        dice1=random.randint(1,6)
                        dice2=random.randint(1,6)
                        self.diceval=dice1+dice2
                        print(self.name,"rolled",dice1,"and",dice2)
                        
                        if(dice1==dice2):
                                doubles+=1
                                if doubles<3:
                                        self.update_position()
                                        print("Doubles! Rolling again")
                                else:
                                        print("Go to jail for speeding")
                                        self.go_to_jail()
                        else:
                                self.update_position()                  



   

        def build(self):   ##Functions used here- get_buildable_assets(),build_on_these()
                buildable_assets=self.get_buildable_assets()
                if(len(buildable_assets)==0):
                    print("No assets to build on.")
                    print("You need all properties of 1 colour to start building")
                    print()
                    print("Returning to move selection")
                    print()
                    return()
                print("You can build 1 house/hotel on the following properties")
                if len(buildable_assets)>0:
                        print("Sr.No.\tName\t\t\t\tHouses\tHotels")
                for i,ba in enumerate(buildable_assets):
                        print(str(i+1)+"\t"+ba.name+" "*(32-len(ba.name))+str(ba.houses)+"\t"+str(ba.hotels))
                print("Enter the serial number of the property you wish to build (space separated for multiple)")
                ch=True
                while(ch):
                        build_on=Player.validate_int_array_input(1,len(buildable_assets))
                        if len(build_on)==0:
                                print("Back to moves selection")
                                return
                        else:
                                flag=0
                                for b in build_on:
                                        if b>len(buildable_assets) or b<=0:
                                                flag=1
                                                print("Invalid input")
                                                break
                                if flag==1:
                                        continue
                                else:
                                        self.build_on_these(buildable_assets,build_on)
                                        ch=False


        def sell(self):
                sellable_assets=self.get_sellable_assets()
                if(len(sellable_assets)==0):
                    print("No assets to sell houses on.")
                    #print("You need all properties of 1 colour to start building")
                    print()
                    print("Returning to move selection")
                    print()
                    return()
                print("You can sell 1 house/hotel on the following properties")
                if len(sellable_assets)>0:
                        print("Sr. No.\tName\t\t\t\tHouses\tHotels")
                for i,ba in enumerate(sellable_assets):
                        print(str(i+1)+"\t"+ba.name+" "*(32-len(ba.name))+str(ba.houses)+"\t"+str(ba.hotels))
                print("Enter the serial number of the property you wish to sell (space separated for multiple)")
                ch=True
                while(ch):
                        sell_on=Player.validate_int_array_input(1,len(sellable_assets))
                        if len(sell_on)==0:
                                print("Back to moves selection")
                                return
                        else:
                                flag=0
                                for b in sell_on:
                                        if b>len(sellable_assets) or b<=0:
                                                flag=1
                                                print("Invalid input")
                                                break
                                if flag==1:
                                        continue
                                else:
                                        self.sell_on_these(sellable_assets,sell_on)
                                        ch=False

        def mortgage(self):
                mortgageable_assets=self.get_mortgageable_assets()
                if(len(mortgageable_assets)==0):
                    print("No assets to mortgage.")
                    #print("You need all properties of 1 colour to start building")
                    print()
                    print("Returning to move selection")
                    print()
                    return()
                print("You can mortgage the following properties")
                if len(mortgageable_assets)>0:
                        print("Sr. No.\tName")
                for i,ba in enumerate(mortgageable_assets):
                        print(i+1,ba.name)
                print("Enter the serial number of the property you wish to mortgage (space separated for multiple)")
                ch=True
                while(ch):
                        mortgage_on=Player.validate_int_array_input(1,len(mortgageable_assets))
                        if len(mortgage_on)==0:
                                print("Back to moves selection")
                                return
                        else:
                                flag=0
                                for b in mortgage_on:
                                        if b>len(mortgageable_assets) or b<=0:
                                                flag=1
                                                print("Invalid input")
                                                break
                                if flag==1:
                                        continue
                                else:
                                        self.mortgage_on_these(mortgageable_assets,mortgage_on)
                                        ch=False

        def redeem(self):
                redeemable_assets=self.get_redeemable_assets()
                if(len(redeemable_assets)==0):
                    print("No assets to redeem.")
                    #print("You need all properties of 1 colour to start building")
                    print()
                    print("Returning to move selection")
                    print()
                    return()
                print("You can redeem the following properties")
                if len(redeemable_assets)>0:
                        print("Sr.No.\tName")
                for i,ba in enumerate(redeemable_assets):
                        print(str(i+1)+"\t"+ba.name)
                print("Enter the serial number(s) of the property you wish to redeem (space separated for multiple)")
                ch=True
                while(ch):
                        redeem_on=Player.validate_int_array_input(1,len(redeemable_assets))
                        if len(redeem_on)==0:
                                print("Back to moves selection")
                                return
                        else:
                                flag=0
                                for b in redeem_on:
                                        if b>len(redeemable_assets) or b<=0:
                                                flag=1
                                                print("Invalid input")
                                                break
                                if flag==1:
                                        continue
                                else:
                                        self.redeem_on_these(redeemable_assets,redeem_on)
                                        ch=False


        def jailoptions(self):
                self.position=10
                tmv=self.total_mortgageable_value()
                card=self.jailfreecard                      ##Array of types of jailfree cards
                print("Do you want to:","roll for doubles(r)",sep="\n")
                if(self.cash>=50):
                        print("pay Rs50 and get out of jail(p)")
                if(len(card)>=1):
                        print("use jailfree card(c)")

                ch=True
                while(ch):
                        ch=False
                        choice=input()
                        if choice=="r":
                                self.diceval=0
                                dice1=0
                                dice2=0
                                dice1=random.randint(1,6)
                                dice2=random.randint(1,6)
                                print(self.name,"rolled",dice1,"and",dice2)

                                if(dice1==dice2):
                                        print("You rolled a double!!")
                                        self.injail=0
                                        self.diceval=dice1+dice2
                                        self.update_position()

                                else:
                                        print("Sorry! You did not roll a double")
                                        print("Back to moves selection")
                                        self.injail-=1

                        elif choice=="p" and (self.cash>=50):
                            self.injail=0
                            self.cash-=50
                            #self.roll()

                        elif choice=="c" and (len(card)>=1):
                            self.injail=0
                            return_card=self.jailfreecard.pop()
                            Cards.Cards.return_jailfree(return_card)
                            #self.roll()

                        else:
                            ch=True
                            print("Illegal value entered")

        def request_properties_and_money(self,tradee):
                print("Please enter the serial no. of the properties you want")
                print("Space separated for multiple properties,then press enter")
                tradable=tradee.get_tradable_assets()
                print(tradee.name+"'s assets")
                self.show_assets(tradable)
                req_prop=[]
                err=1
                while(err==1):
                    req_prop_ind=Player.validate_int_array_input(1,len(tradable))
                    flag=0
                    for ind in req_prop_ind:
                        if ind<=0 or ind>len(tradable):
                            flag=1
                            print("Incorrect input,please input again")
                            break

                    if(flag==0):
                        err=0
                        for ind in req_prop_ind:
                            req_prop.append(tradable[ind-1])

                        print("Enter amount you want from",tradee.name,"(0 if you want to give money)")
                        print("integer only")
                        req_money=Player.validate_int_input(0,tradee.cash)
                        req_prop.append(req_money)
                return(req_prop)


        def togive_properties_and_money(self,tradee):
                print("Please enter the serial no. of the properties you want to give")
                print("Space separated for multiple properties,then press enter")
                tradable=self.get_tradable_assets()
                print(self.name+"'s assets")
                self.show_assets(tradable)
                togive_prop=[]
                err=1
                while(err==1):
                    togive_prop_ind=Player.validate_int_array_input(1,len(tradable))
                    flag=0
                    for ind in togive_prop_ind:
                        if ind<=0 or ind>len(tradable):
                            flag=1
                            print("Incorrect input,please input again")
                            break

                    if(flag==0):
                        err=0
                        for ind in togive_prop_ind:
                            togive_prop.append(tradable[ind-1])

                        print("Enter amount you want to give to",tradee.name,"(0 if you want to ask for money)")
                        print("integer only")
                        togive_money=Player.validate_int_input(0,self.cash)
                        togive_prop.append(togive_money)
                return(togive_prop)

        def present_trade(self,trader,requested_properties,togive_properties,requested_money,togive_money):
                print(trader.name,"wants to trade with you")
                print("You get:")
                print("Money=",togive_money)
                print("Properties:")
                #print(togive_properties)
                self.show_assets(togive_properties)
                print()
                print("You give:")
                print("Money=",requested_money)
                print("Properties:")
                #print(requested_properties)
                self.show_assets(requested_properties)
                print()
                print("Here are your assets for reference")
                self.show_my_assets()
                print("Do you accept this trade?(Y/N)")
                agreed_status=True if input().lower()=="y" else False
                return(agreed_status)

        def get_bid(self,property,highest_bid):
                bid=-1
                while(bid<=highest_bid and bid!=0):
                    print("Your bid(0 to fold)=")
                    bid=Player.validate_int_input(0,self.cash)
                    if bid<=highest_bid:
                        print("You have to bid higher than the highest bid(Rs"+str(highest_bid)+") or fold")
                return(bid)

        def chance_or_10(self):
                        print("Enter 'c' to take a chance and 'p' to pay fine")
                        ch=None
                        while(True):
                                ch=input()
                                if ch!="c" and ch!="p":
                                        print("Invalid input. Enter 'c' for chance or 'p' to pay fine")
                                else:
                                        break
                        if(ch==None):
                                print("Error in chance_or_10 function")
                        return(ch)
                                




class Machine(Player):
        def __init__(self,name):
            Player.__init__(self,name,"Machine")
            self.other_players=[]
            self.move=0


        def fill_other_players(self):
            self.other_players=PlayerInteraction.PlayerInteraction.get_other_players(self)

        def make_move(self):
            self.move+=1
            #if self.move%5==0:
            #    self.show_my_assets()
            if self.cash<0 and self.cash+self.total_mortgageable_value()>=0:
                    while(self.cash<0):
                            self.mortgage(0-self.cash)
                            self.sell(0-self.cash)

            elif self.cash<0 and self.cash+self.total_mortgageable_value()<0:
                    return()

            if self.injail>0:
                self.jailoptions()

            self.fill_other_players()
            if self.injail==0:
                self.roll()
            self.redeem()
            self.build()
            trade=random.choice([1]*1+[0]*4)
            if trade==1:
                PlayerInteraction.PlayerInteraction.trade(self)
            #self.

                       
        def decide_to_buy(self,property,mode):
            if mode==1:
                decision=random.choice(["yes"]*5+["no"]*3)
                return(decision)
            else:
                if self.only_mortgageable_value()+self.cash>property.price:
                    decision=random.choice(["yes"]*1+["no"]*1)
                    if decision=="yes":
                        while(self.cash<property.price):
                            self.mortgage(property.price-self.cash)
                            self.sell(property.price-self.cash)


                    return(decision)

                else:
                    decision=random.choice(["yes"]*1+["no"]*4)
                    if decision=="yes":
                        while(self.cash<property.price):
                            self.mortgage(property.price-self.cash)
                            self.sell(property.price-self.cash)

                    return(decision)
                    

        def only_mortgageable_value(self):
            value=0
            for asset in self.asset_list:
                if asset.mortgaged_status==0:
                    value+=asset.get_mortgage_val()

            return(value)

        def roll(self):
                self.diceval=0
                dice1=0
                dice2=0
                doubles=0
                while(dice1==dice2 and doubles<3):
                        dice1=random.randint(1,6)
                        dice2=random.randint(1,6)
                        self.diceval=dice1+dice2
                        print(self.name,"rolled",dice1,"and",dice2)
                        
                        if(dice1==dice2):
                                doubles+=1
                                if doubles<3:
                                        self.update_position()
                                        print("Doubles! Rolling again")
                                else:
                                        print("Go to jail for speeding")
                                        self.go_to_jail()
                        else:
                                self.update_position()                  



   

        def build(self):   ##Functions used here- get_buildable_assets(),build_on_these()
                buildable_assets=self.get_buildable_assets()
                if(len(buildable_assets)==0):
                    return()
                else:
                    buildable_assets=sorted(buildable_assets, key=lambda asset:asset.houseval())
                    build_on=[]
                    money=self.cash
                    i=0
                    while(money>200 and i<len(buildable_assets)):
                        money-=buildable_assets[i].houseval()
                        build_on.append(i)
                        i+=1
                    self.build_on_these(buildable_assets,build_on)



        def sell(self,target_val):
                #print()
                #print(self.name,"is selling")
                sellable_assets=self.get_sellable_assets()


                if target_val<=0 or len(sellable_assets)==0:
                    return()

                #for asset in sellable_assets:
                    #print(asset.name)
                
                sell_val=0
                ind=0
                for i,asset in enumerate(sellable_assets):
                    sell_val+=asset.houseval()
                    if sell_val>target_val:
                        #print("sell1")
                        self.sell_on_these(sellable_assets,range(1,ind+2))
                        return()
                #print("sell2")
                self.sell_on_these(sellable_assets,range(1,len(sellable_assets)+1))

        def mortgage(self,target_val):
                mortgageable_assets=self.get_mortgageable_assets()

                if target_val<=0 or len(mortgageable_assets)==0:
                    return()
                mort_val=0
                ind=0
                for i,asset in enumerate(mortgageable_assets):
                    mort_val+=asset.get_mortgage_val()
                    if mort_val>target_val:
                        self.mortgage_on_these(mortgageable_assets,range(1,ind+2))
                        return()

                self.mortgage_on_these(mortgageable_assets,range(1,len(mortgageable_assets)+1))

        def redeem(self):
                redeemable_assets=self.get_redeemable_assets()
                if len(redeemable_assets)==0:
                    return()
                redeemable_assets=sorted(redeemable_assets, key=lambda asset:asset.price)
                decision=[0]*len(redeemable_assets)
                for player in self.other_players:
                    pos=player.position
                    end=(player.position+12)%40
                    for i,asset in enumerate(redeemable_assets):
                        aspos=asset.position
                        if end<pos:
                            if aspos<=end or aspos>pos:
                                distance=aspos-pos if aspos>pos else aspos-pos+40
                                num=distance-1 if distance<=7 else 13-distance
                                if(num<0 or num>6):
                                    num=0
                                decision[i]+=random.choice([1]*num+[0]*(36-num))

                        elif end>pos:
                            if aspos<=end and aspos>pos:
                                distance=aspos-pos
                                num=distance-1 if distance<=7 else 13-distance
                                if(num<0 or num>6):
                                    num=0
                                decision[i]+=random.choice([1]*num+[0]*(36-num))

                        else:
                            print("ERROR in redeem machine function")


                want_to_redeem=[]
                redeem_val=0
                for i in range(len(decision)):
                    if decision[i]>0:
                        redeem_val+=redeemable_assets[i].get_mortgage_val()*1.1
                        if redeem_val<self.cash:
                            want_to_redeem.append(i+1)

                self.redeem_on_these(redeemable_assets,want_to_redeem)





        def jailoptions(self):
                self.position=10
                if(len(self.jailfreecard)>=1):
                    choice="c"
                elif(self.cash>300):
                    choice="p"
                else:
                    choice="r"

                if choice=="r":
                        print(self.name,"chose to roll the dice")
                        self.diceval=0
                        dice1=0
                        dice2=0
                        dice1=random.randint(1,6)
                        dice2=random.randint(1,6)
                        print(self.name,"rolled",dice1,"and",dice2)

                        if(dice1==dice2):
                                print(self.name,"rolled a double!!")
                                self.injail=0
                                self.diceval=dice1+dice2
                                self.update_position()

                        else:
                                print(self.name,"did not roll a double")
                                self.injail-=1

                elif choice=="p" and (self.cash>=50):
                    print(self.name,"chose to pay Rs50 and get out of jail")
                    self.injail=0
                    self.cash-=50
                    #self.roll()

                elif choice=="c" and (len(self.jailfreecard)>=1):
                    print(self.name,"chose to use jailfree card to get out of jail")
                    self.injail=0
                    return_card=self.jailfreecard.pop()
                    Cards.Cards.return_jailfree(return_card)
                    #self.roll()

                else:
                    ch=True
                    print("Illegal value entered")






        def request_properties_and_money(self,tradee):
                print("Please enter the serial no. of the properties you want")
                print("Space separated for multiple properties,then press enter")
                tradee.show_my_assets()
                req_prop=[]
                err=1
                while(err==1):
                    req_prop_ind=Player.validate_int_array_input(1,len(tradee.asset_list))
                    flag=0
                    for ind in req_prop_ind:
                        if ind<=0 or ind>len(tradee.asset_list):
                            flag=1
                            print("Incorrect input,please input again")
                            break

                    if(flag==0):
                        err=0
                        for ind in req_prop_ind:
                            req_prop.append(tradee.asset_list[ind-1])

                        print("Enter amount you want from",tradee.name,"(0 if you want to give money)")
                        print("integer only")
                        req_money=Player.validate_int_input(0)
                        req_prop.append(req_money)
                return(req_prop)    


        def togive_properties_and_money(self,tradee):
                print("Please enter the serial no. of the properties you want to give")
                print("Space separated for multiple properties,then press enter")
                self.show_my_assets()
                togive_prop=[]
                err=1
                while(err==1):
                    togive_prop_ind=Player.validate_int_array_input(1,len(self.asset_list))
                    flag=0
                    for ind in togive_prop_ind:
                        if ind<=0 or ind>len(self.asset_list):
                            flag=1
                            print("Incorrect input,please input again")
                            break

                    if(flag==0):
                        err=0
                        for ind in togive_prop_ind:
                            togive_prop.append(self.asset_list[ind-1])

                        print("Enter amount you want to give to",tradee.name,"(0 if you want to ask for money)")
                        print("integer only")
                        togive_money=Player.validate_int_input(0)
                        togive_prop.append(togive_money)
                return(togive_prop)

        def present_trade(self,trader,requested_properties,togive_properties,requested_money,togive_money):
                flag=0                                      ##Higher flag value means that the computer is willing to do the trade
                req_value=0
                togive_value=0
                for prop in requested_properties:
                    if(self.check_group(prop,2,3,3,2)):
                        return(False)
                    elif(self.check_group(prop,1,2,2,1)):
                        req_value+=prop.get_value()
                        flag-=3
                    else:
                        req_value+=prop.get_value()
                        flag-=1
                    #print("Flag is",flag)
                #print("how")

                for prop in togive_properties:
                    if(self.check_group(prop,1,2,3,1)):
                        return(True)
                    elif(self.check_group(prop,0,1,1,0)):
                        togive_value+=prop.get_value()
                        flag+=3
                    else:
                        togive_value+=prop.get_value()
                        flag+=1
                    #print("Flag is",flag)
                #print("hi")

                if(requested_money!=0):
                    #print("requested_money=",requested_money,"togive_value=",togive_value)
                    flag+=int((togive_value*2.5)/requested_money)-4
                #print("Flag is",flag)

                if(togive_money!=0):
                    #print("togive_money=",togive_money,"requested_value=",req_value)
                    flag-=int((req_value*2.5)/togive_money)-4
                #print("Flag is",flag)

                if(flag>=0):
                    return(True)
                else:
                    return(False)



                    
                



        


        def get_bid(self,property,highest_bid):
                bid=None
                if self.cash<=highest_bid:
                    return(0)
                else:
                    if self.check_group(property,1,2,2,1)==1:
                        return(highest_bid+int((0.1)*(self.cash-highest_bid)))
                    else:
                        intended_bid=highest_bid+int((0.1)*(property.price)) if (highest_bid<property.price and self.cash>1.1*property.price) else highest_bid+int((0.1)*(self.cash-highest_bid))
                        probability=((property.price-intended_bid)/property.price)*0.5+0.5
                        if(probability<0):
                            probability=0
                        yes=int(probability*100)
                        dec=random.choice([1]*yes+[0]*(100-yes))
                        if dec==1:
                            return(intended_bid)
                        else:
                            return(0)

        def givable_properties(self):
                givable=[]
                for asset in self.asset_list:
                        if self.check_group(asset,2,3,3,2)==0:
                                givable.append(asset)
                return(givable)

        def find_val(self,assets):
                value=0
                for asset in assets:
                        value+=asset.get_value()
                return(value)

        def trade_decisions(self,trade_proposal):
                givable=self.givable_properties()
                givable_val=self.cash+self.find_val(givable)
                gettable_val=1000000000
                trade_try=1
                tradee=None
                requested=[]
                while(gettable_val>givable_val):
                        if trade_try>5:
                                return()
                        #print(self.other_players)
                        #print("Hi")
                        tradee=random.choice(self.other_players)
                        requested=[]
                        l=len(tradee.asset_list)
                        if l==0:
                                tradee=None
                                return()
                        req_asset=random.choice(tradee.asset_list)
                        while(req_asset not in requested and len(requested)<min(l,2) and (req_asset.type!="Residence" or req_asset.houses==0)):
                                requested.append(req_asset)
                                req_asset=random.choice(tradee.asset_list)
                        gettable_val=self.find_val(requested)
                        #print()
                        #print(tradee.name)
                        #for asset in requested:
                        #       print(asset.name)
                        #print("gettable_val=",gettable_val,"givable_val=",givable_val)
                        trade_try+=1
                if tradee==None:
                        return()
                else:
                        trade_proposal.tradee=tradee
                        trade_proposal.requested_properties=requested

                        give=[]
                        givable=sorted(givable,key=lambda asset:asset.get_value())
                        val=0
                        i=0
                        while(val<gettable_val and i<len(givable)):
                                give.append(givable[i])
                                val+=givable[i].get_value()
                                i+=1
                        trade_proposal.togive_properties=give
                        if val>gettable_val:
                                trade_proposal.requested_money=(val-gettable_val)
                        else:
                                trade_proposal.togive_money=gettable_val-val

















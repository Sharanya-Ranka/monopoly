import random
import copy
import PlayerInteraction

class Cards():
        community_chest_cards=[]
        chance_cards=[]
        is_jailfree_in_deck=[1,1]                       ##Flag for whether jailfree card is in deck or not [comm_chest,chance]
      
        @staticmethod
        def fill_cards():
                Cards.community_chest_cards.append(['goto 0',"Advance to 'Go'"])
                Cards.community_chest_cards.append(['goto 1',"Go back to Old Kent Road"])
                Cards.community_chest_cards.append(['goto -1',"Go to jail. Move directly to jail. Do not pass 'Go'. Do not collect Rs200"])
                Cards.community_chest_cards.append(['pay 100',"Pay hospital Rs 100"])
                Cards.community_chest_cards.append(['pay 50',"Doctor's fee. Pay Rs 50"])
                Cards.community_chest_cards.append(['pay 50',"Pay your insurance premium Rs 50"])
                Cards.community_chest_cards.append(['receive 200',"Bank error in your favour. Collect Rs 200"])
                Cards.community_chest_cards.append(['receive 100',"Annuity matures. Collect Rs 100"])
                Cards.community_chest_cards.append(['receive 100',"You inherit Rs 100"])
                Cards.community_chest_cards.append(['receive 50',"From sale of stock you get Rs 50"])
                Cards.community_chest_cards.append(['receive 25',"Receive interest on 7% preference shares: Rs 25"])
                Cards.community_chest_cards.append(['receive 20',"Income tax refund. Collect Rs 20"])
                Cards.community_chest_cards.append(['receive 10',"You have won second prize in a beauty contest. Collect Rs 10"])
                Cards.community_chest_cards.append(['birthday',"It is your birthday. Collect Rs 10 from each player"])
                Cards.community_chest_cards.append(['jailfree',"Get out of jail free. This card may be kept until needed or sold"])
                Cards.community_chest_cards.append(['chance_or_10',"Pay a Rs 10 fine or take a 'Chance'"])

                Cards.chance_cards.append(['goto 0',"Advance to 'Go'"])
                Cards.chance_cards.append(['goto -1',"Go to jail. Move directly to jail. Do not pass 'Go'. Do not collect Rs 200"])
                Cards.chance_cards.append(['goto 11',"Advance to Pall Mall. If you pass 'Go' collection Rs 200"])
                Cards.chance_cards.append(['goto 15',"Take a trip to Marylebone Station and if you pass 'Go' collect Rs 200"])
                Cards.chance_cards.append(['goto 24',"Advance to Trafalgar Square. If you pass 'Go' collect Rs 200"])
                Cards.chance_cards.append(['goto 39',"Advance to Mayfair"])
                Cards.chance_cards.append(['goto -1',"Go back three spaces"])
                Cards.chance_cards.append(['repairs 25 100',"Make general repairs on all of your houses. For each house pay Rs 25. For each hotel pay Rs 100"])
                Cards.chance_cards.append(['repairs 40 115',"You are assessed for street repairs: Rs 40 per house, Rs 115 per hotel"])
                Cards.chance_cards.append(['pay 150',"Pay school fees of Rs 150"])
                Cards.chance_cards.append(['pay 20',"'Drunk in charge' fine Rs 20"])
                Cards.chance_cards.append(['pay 15',"Speeding fine Rs 15"])
                Cards.chance_cards.append(['receive 150',"Your building loan matures. Receive Rs 150"])
                Cards.chance_cards.append(['receive 100',"You have won a crossword competition. Collect Rs 100"])
                Cards.chance_cards.append(['receive 50',"Bank pays you dividend of Rs 50"])
                Cards.chance_cards.append(['jailfree',"Get out of jail free. This card may be kept until needed or sold"])
               

        def getcards(self):
                with open(self.fileloc,'r') as f:
                        for line in f:
                                if line.trim() !="":
                                        signature,text=line.split()
                                        self.list_of_cards.append([signature,text])

                self.number=len(self.list_of_cards)

        @staticmethod
        def randomize():
                temp=[]
                while(len(Cards.community_chest_cards)>0):
                        ch=random.choice(Cards.community_chest_cards)
                        Cards.community_chest_cards.remove(ch)
                        temp.append(ch)
                Cards.community_chest_cards=copy.deepcopy(temp)
                temp=[]
                while(len(Cards.chance_cards)>0):
                        ch=random.choice(Cards.chance_cards)
                        Cards.chance_cards.remove(ch)
                        temp.append(ch)
                Cards.chance_cards=copy.deepcopy(temp)
                temp=[]


        @staticmethod
        def pickcard(cardtype,player):         ##Will pick a card from top of stack and will perform actions on player accordingly
                                                                ##player is an object of Player type  
                                                                ##Yet have to do birthday and take 10 fine or chance
                card=["er","er"]
                if cardtype.lower()=="community chest":
                        card=Cards.community_chest_cards.pop()
                        if card[0]!="jailfree":
                                Cards.community_chest_cards.insert(0,card)
                        else:
                                Cards.is_jailfree_in_deck[0]=0

                elif cardtype.lower()=="chance":
                        card=Cards.chance_cards.pop()
                        if card[0]!="jailfree":
                                Cards.chance_cards.insert(0,card)
                        else:
                                Cards.is_jailfree_in_deck[1]=0

                print("You picked '",card[1],"'")
                sig=card[0]
                if sig.split()[0]=="pay":
                        player.cash-=int(sig.split()[1])         ##Player should contain pay() function

                elif sig.split()[0]=="receive":
                        player.cash+=int(sig.split()[1])     ##Player should contain receive() function

                elif sig.split()[0]=="goto":
                        position=int(sig.split()[1])
                        if position==-1:                                        ##Go to jail
                                player.go_to_jail()
                        elif position==1:                                       ##Go back to Old Kent Road
                                player.diceval=1-player.position
                                player.update_position()
                        elif position==-3:                                      ##Go back 3 spaces
                                player.diceval=-3
                                player.update_position()
                        else:                                                           ##Normal case
                                if player.position>position:
                                        player.diceval=40-player.position+position
                                else:
                                        player.diceval=position-player.position
                                player.update_position()

                elif sig.split()[0]=="repairs":
                        house_cost=int(sig.split()[1])
                        hotel_cost=int(sig.split()[2])
                        houses=0
                        hotels=0
                        for asset in player.asset_list:
                                if asset.type=="Residence":
                                        houses+=asset.get_houses()
                                        hotels+=asset.get_hotels()
                        player.cash-=(houses*house_cost)+(hotels*hotel_cost)

                elif sig.split()[0]=="jailfree":
                        player.jailfreecard.append(cardtype)
                        #print("At jailfree")
                elif sig.split()[0]=="chance_or_10":
                        if player.type=="Machine":
                                ch="c"
                        else:
                                ch=player.chance_or_10()
                        if ch=="c":
                                Cards.pickcard("Chance",player)
                        elif ch=="p":
                                player.cash-=10
                        else:
                                print("Invalid value for chance_or_10")

                elif sig.split()[0]=="birthday":
                        other_players=PlayerInteraction.PlayerInteraction.get_other_players(player)
                        for pl in other_players:
                                pl.cash-=10
                                player.cash+=10
                else:
                        print("No card taken")



        @staticmethod
        def return_jailfree(cardtype):
                if cardtype=="Community Chest":
                        Cards.is_jailfree_in_deck[0]=1
                        Cards.community_chest_cards.insert(0,['jailfree',"Get out of jail free. This card may be kept until needed or sold"])

                elif cardtype=="Chance":
                        Cards.is_jailfree_in_deck[1]=1
                        Cards.chance_cards.insert(0,['jailfree',"Get out of jail free. This card may be kept until needed or sold"])





import TradeProposal
import copy



class PlayerInteraction:
        list_of_players=[]

        @staticmethod
        def trade(trader):
                        if trader.type=="Human":
                                print("Here are all players' tradable_assets")
                                for pl in PlayerInteraction.list_of_players:
                                        print(pl.name+"s assets")
                                        tr=pl.get_tradable_assets()
                                        pl.show_assets(tr)
                                print("Enter the sr.no of the player you want to trade with")
                                for i,pl in enumerate(PlayerInteraction.list_of_players):
                                        print(i+1,pl.name)

                                check=False
                                while(check==False):
                                        try:
                                                n=int(input())
                                        except ValueError:
                                                print("Invlid choice")
                                        if n<0 or n>len(PlayerInteraction.list_of_players):
                                                print("Incorrect choice, choose again(press 0 if not trading)")
                                        elif n==0:
                                                return()
                                        elif PlayerInteraction.list_of_players[n-1]==trader:
                                                print("Cannot trade with yourself")
                                        else:
                                                tradee=PlayerInteraction.list_of_players[n-1]
                                                check=True

                                trade_proposal=TradeProposal.TradeProposal(trader,tradee)
                                trade_proposal.request_properties_and_money()
                                trade_proposal.togive_properties_and_money()
                                trade_proposal.present_trade()
                        else:
                                trade_proposal=TradeProposal.TradeProposal(trader,None)
                                trader.trade_decisions(trade_proposal)
                                if trade_proposal.tradee==None:
                                        return()
                                trade_proposal.present_trade()


        @staticmethod
        def auction(property,initiating_player=None):##Assumes property belongs to bank first

                print("Auctioning",property.name)
                print("Value of property=",property.get_value())
                if initiating_player!=None:
                        i=PlayerInteraction.list_of_players.index(initiating_player)
                        start=copy.copy(PlayerInteraction.list_of_players[i:])
                        end=copy.copy(PlayerInteraction.list_of_players[:i])
                        players_in_auction=start+end
                else:
                        players_in_auction=copy.copy(PlayerInteraction.list_of_players)
                highest_bid=0
                while(len(players_in_auction)>1):
                        for player in players_in_auction:
                                if len(players_in_auction)==1:
                                        break

                                bid=player.get_bid(property,highest_bid)

                                if bid==0:
                                        print(player.name," has exited the auction.")
                                        players_in_auction.remove(player)
                                else:
                                                if(bid>highest_bid):
                                                        print(player.name," bids Rs",bid)
                                                        highest_bid=bid

                if(len(players_in_auction)!=1):
                        print("ERROR, length of players_in_auction=",len(players_in_auction))
                winner=players_in_auction[0]
                print(winner.name,"has won the auction for",property.name)
                #print(winner)
                property.owner=winner
                #print(property.owner)
                winner.asset_list.append(property)
                #print("showing properties")
                #for asset in winner.asset_list:
                #        print(asset.name)
                winner.cash-=highest_bid

        @staticmethod
        def show_all_assets():
                for  pl in PlayerInteraction.list_of_players:
                                
                                pl.show_my_assets()

        @staticmethod
        def get_other_players(pl):
                reqlist=[]
                for player in PlayerInteraction.list_of_players:
                        if player==pl:
                                continue
                        else:
                                reqlist.append(player)
                return(reqlist)












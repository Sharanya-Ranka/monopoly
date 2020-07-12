import Player
import Properties
import PlayerInteraction
import Cards
import random
import Tiles
import time

class GameBoard():
        def __init__(self):
                #self.tiles={}                           ##List of all tiles on the gameboard
                self.players=[]                         ##List  of all players playing the game(will be given by Game class)
                self.bankrupt_players=[]

        
        def game_setup(self):
                print("LET'S PLAY MONOPOLY!")
                while(True):
                        try:
                                print("Enter number of players")
                                n=int(input())
                                print("Enter number of human players(others will be machine-players)")
                                h=int(input())
                                break
                        except ValueError:
                                print("Please enter valid inputs")
                if(h<0 or n<=1):
                        print("Invalid values provided, taking total players as 2 and humans as 1")
                        n=2
                        h=1     
                if(h>n):
                        print("Human players cannot be more than total players,setting humans==total players")
                        h=n

                pl={}
                for ind in range(h):
                        print("Enter name of Human Player",ind+1)
                        name=input()
                        if name=="":
                                name="Human"+str(ind+1)
                        player=Player.Human(name)
                        pl[player]=random.randint(1,6)+random.randint(1,6)

                for ind in range(n-h):
                        print("Enter name of Machine Player",ind+1)
                        name=input()
                        if name=="":
                                name="Machine"+str(ind+1)
                        player=Player.Machine(name)
                        pl[player]=random.randint(1,6)+random.randint(1,6)

                print("Options in move selection")
                print("roll_die(roll)-Must be done once each turn(except in jail)")
                print("my_assets(ma)- View your assets")
                print("all_players'_assets(a)- View all players' assets")
                print("finish_turn(f)-finish your turn")
                print("build(b)- If you want to build houses or hotels")
                print("sell(s)- If you want to sell houses or hotels")
                print("mortgage(m)- If you want to mortgage properties")
                print("redeem(r)- If you want to redeem properties")
                print("trade(t)-If you want to trade with a player")
                print("exit(e)- Exit the game(game won't be saved)")
                print()
                print()

                time.sleep(2)

                print("Rolling for turn-order")

                for player in pl:
                        print(player.name,"rolled",pl[player])

                self.players=sorted(pl,key=lambda v:pl[v],reverse=True)
                print(self.players[0].name+" has highest roll and will play first")
                print()

                Cards.Cards.fill_cards()
                Cards.Cards.randomize()
                Tiles.Tiles.fill_tiles()
                PlayerInteraction.PlayerInteraction.list_of_players=self.players
                self.play_game()

        

        def play_game(self):
                winner=None
                #nextround=True
                while(len(self.players)>1):
                        #print(len(self.players))
                        for player in self.players:
                                bankrupt=player.isbankrupt()                            ##make_move should also check for injail
                                if bankrupt==True:
                                        print(player.name,"has gone bankrupt")
                                        print()
                                        self.bankrupt_players.append(player)
                                        self.players.remove(player)
                                        #PlayerInteraction.PlayerInteraction.list_of_players=self.players
                                        player.auction_all_properties()
                                else:
                                        player.make_move()
                                if len(self.players)==1:
                                        winner=self.players[0]
                                        break
                                print("-----"+player.name+" has finished turn-----")
                                print()
                        print("----------------------Round complete---------------------")
                        print()

                        # count=0
                        # for player in GameBoard.players:
                        #       if player.isbankrupt():
                        #               count+=1

                        # if count>=len(GameBoard.players)-1:           ##If all (or all but one player) are bankrupt, stop game 
                        #       nextround=False
                print("Winner is",winner.name)
                print("GAME HAS ENDED")

New_Game=GameBoard()
New_Game.game_setup()

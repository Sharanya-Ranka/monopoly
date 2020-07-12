import GameBoard
import Player
import random
import Cards

class Game():

        def game_setup(self):
                print("LET'S PLAY MONOPOLY!")
                print("Enter number of players")
                n=int(input())
                print("Enter number of human players(others will be machine-players)")
                h=int(input())
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
                        player=Player.Human(name)
                        pl[player]=random.randint(1,6)+random.randint(1,6)

                print("Rolling for turn-order")

                for player in pl:
                        print(player.name,"rolled",pl[player])

                GameBoard.players=sorted(pl,key=lambda v:pl[v],reverse=True)

                Cards.Cards.fill_cards()
                GameBoard.GameBoard.fill_tiles()
                GameBoard.GameBoard.play_game()


NewGame=Game()
NewGame.game_setup()

import Properties
#import PlayerInteraction
import Cards
import random

class GameBoard():
        tiles={}                           ##List of all tiles on the gameboard
        players=[]                         ##List  of all GameBoard.players playing the game(will be given by Game class)
        bankrupt_players=[]

        @staticmethod
        def fill_tiles():               ##Fill in objects of Properties class or Others class
        ##Each tile to have a name and a type atleast
        ##(self,name,price,colour,position,owner,titledeed)
                GameBoard.tiles[0]=Properties.Others("GO",0,"Other")
                GameBoard.tiles[1]=Properties.Residence("Old Kent Road",60,"Brown",1,"Bank",[2,10,30,90,160,250])
                GameBoard.tiles[2]=Properties.Others("Community Chest",2,"Community Chest")
                GameBoard.tiles[3]=Properties.Residence("Whitechapel Road",60,"Brown",3,"Bank",[4,20,60,180,320,450])
                GameBoard.tiles[4]=Properties.Others("Income Tax",4,"Income Tax")
                GameBoard.tiles[5]=Properties.Station("Kings Cross Station",200,"Black",5,"Bank",[0,25,50,100,200])
                GameBoard.tiles[6]=Properties.Residence("The Angel Islington",100,"Light Blue",6,"Bank",[6,30,90,270,400,550])
                GameBoard.tiles[7]=Properties.Others("Chance",7,"Chance")
                GameBoard.tiles[8]=Properties.Residence("Euston Road",100,"Light Blue",8,"Bank",[6,30,90,270,400,550])
                GameBoard.tiles[9]=Properties.Residence("Pentonville Road",120,"Light Blue",9,"Bank",[8,40,100,300,450,600])

                GameBoard.tiles[10]=Properties.Others("Just Visiting",10,"Just Visiting")
                GameBoard.tiles[11]=Properties.Residence("Pall Mall",140,"Pink",11,"Bank",[10,50,150,450,625,750])
                GameBoard.tiles[12]=Properties.Utility("Electric Company",150,"Black",12,"Bank",[])
                GameBoard.tiles[13]=Properties.Residence("Whitehall",140,"Pink",13,"Bank",[10,50,150,450,625,750])
                GameBoard.tiles[14]=Properties.Residence("Northumberland Avenue",160,"Pink",14,"Bank",[12,60,180,500,700,900])
                GameBoard.tiles[15]=Properties.Station("Marylebone Station",200,"Brown",15,"Bank",[0,25,50,100,200])
                GameBoard.tiles[16]=Properties.Residence("Bow Steet",180,"Orange",16,"Bank",[14,70,200,550,750,950])
                GameBoard.tiles[17]=Properties.Others("Community Chest",17,"Community Ches")
                GameBoard.tiles[18]=Properties.Residence("Marlborough Street",180,"Orange",18,"Bank",[14,70,200,550,750,950])
                GameBoard.tiles[19]=Properties.Residence("Vine Street",200,"Orange",19,"Bank",[16,80,220,600,800,1000])
                GameBoard.tiles[20]=Properties.Others("Free Parking",20,"Free Parking")

                GameBoard.tiles[21]=Properties.Residence("The Strand",220,"Red",21,"Bank",[18,90,250,700,875,1050])
                GameBoard.tiles[22]=Properties.Others("Chance",22,"Chance")
                GameBoard.tiles[23]=Properties.Residence("Fleet Street",220,"Red",23,"Bank",[18,90,250,700,875,1050])
                GameBoard.tiles[24]=Properties.Residence("Trafalgar Square",240,"Red",24,"Bank",[20,100,300,750,925,1100])
                GameBoard.tiles[25]=Properties.Station("Fenchurch Street Station",200,"Black",25,"Bank",[0,25,50,100,200])
                GameBoard.tiles[26]=Properties.Residence("Leicester Square",260,"Yellow",26,"Bank",[22,110,330,800,975,1150])
                GameBoard.tiles[27]=Properties.Residence("Coventry Street",260,"Yellow",27,"Bank",[22,110,330,800,975,1150])
                GameBoard.tiles[28]=Properties.Utility("Water Works",150,"Black",28,"Bank",[])
                GameBoard.tiles[29]=Properties.Residence("Piccadilly",280,"Yellow",29,"Bank",[22,120,360,850,1025,1200])
                GameBoard.tiles[30]=Properties.Others("Go to Jail",30,"Go to Jail")
                
                GameBoard.tiles[31]=Properties.Residence("Regent Street",300,"Green",31,"Bank",[26,130,390,900,1100,1275])
                GameBoard.tiles[32]=Properties.Residence("Oxford Street",300,"Green",32,"Bank",[26,130,390,900,1100,1275])
                GameBoard.tiles[33]=Properties.Others("Community Chest",33,"Community Chest")
                GameBoard.tiles[34]=Properties.Residence("Bond Street",320,"Green",34,"Bank",[28,150,450,1000,1200,1400])
                GameBoard.tiles[35]=Properties.Station("Liverpool Street Station",200,"Black",35,"Bank",[0,25,50,100,200])
                GameBoard.tiles[36]=Properties.Others("Chance",36,"Chance")
                GameBoard.tiles[37]=Properties.Residence("Park Lane",350,"Dark Blue",37,"Bank",[35,175,500,1100,1300,1500])
                GameBoard.tiles[38]=Properties.Others("Super Tax",38,"Super Tax")
                GameBoard.tiles[39]=Properties.Residence("Mayfair",400,"Dark Blue",39,"Bank",[50,200,600,1400,1700,2000])
        

        
        
        @staticmethod
        def play_game():
                nextround=True
                while(nextround):
                        if(len(GameBoard.players)<=1):
                                nextround=False
                                break
                        for player in GameBoard.players:
                                bankrupt=player.isbankrupt()                            ##make_move should also check for injail
                                if bankrupt==True:
                                        bankrupt_players.append(player)
                                        GameBoard.players.remove(player)
                                else:
                                		print("Hi")
                                		player.make_move()

                        # count=0
                        # for player in GameBoard.GameBoard.players:
                        #       if player.isbankrupt():
                        #               count+=1

                        # if count>=len(GameBoard.GameBoard.players)-1:           ##If all (or all but one player) are bankrupt, stop game 
                        #       nextround=False

                print("GAME HAS ENDED")


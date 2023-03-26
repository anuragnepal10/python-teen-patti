import random
import os
import time
import pickle
import csv



# CONSTANTS

FILE_NAME = "Game_Files\\top_card.pkl"
FILE_NAME_2 = "Game_Files\\game_stats.csv"
CENTER = 100
TITLE_WIDTH = 38
GAME_TITLE = "TEEN PATTI CARD GAME BY ANURAG NEPAL"
DELAY = 0.1
COLUMN_SPACES = 25
PERCENTAGE_SPACES = 10

#LISTS

rank_list = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
suit_list = ["♠","♥","♣","♦"]


# DICTIONARIES

card_type_dict = {
    5: "THREE OF A KIND",
    4: "DOUBLE RUN",
    3: "RUN",
    2: "FLUSH",
    1: "PAIR CARD",
    0: "HIGH CARD"
}



# TECHNICAL FUNCTIONS

def title():
    
    os.system("cls")
    print(("-"*TITLE_WIDTH).center(CENTER))
    print(GAME_TITLE.center(CENTER))
    print(("-"*TITLE_WIDTH).center(CENTER))
    print("\n\n")

def invalid():
    
    print("Invalid Choice !!".center(CENTER))

def play_again():

    print("\nPlay again?\nPress 'Enter' to play again,\nPress 'q' to quit.")
    user_choice = input().lower()
    if user_choice == "q":
        return False
    else:
        return True

def gap():
    time.sleep(DELAY)


# GAME FUNCTIONS

def isTrial(dict):
    for i in range(2,15):
        if dict[i] ==3:
            return True
    return False

def isStraight(dict):
    for i in range(1,13):
        if all(dict[k] == 1 for k in [i,i+1,i+2]):
            return True
    return False

def isFlush(self):
    if all (self.hand_cards[0].suit == self.hand_cards[i].suit for i in [1,2]):
        return True
    else:
        return False

def isPair(dict):
    for i in range (2,15):
        if dict[i] == 2:
            return True
    False

def scan_winner(players):


    temp_list = players[:]
    temp_list.sort(key=lambda player: player.hand_cards_value(),reverse = True)
    temp_list.sort(key=lambda player: player.hand_cards_type(),reverse = True)
    return temp_list[0]

def high_score_updater(winner):
    is_high_score = False
    if os.path.getsize(FILE_NAME) == 0:
            is_high_score= True       
    else:
        high_score = high_score_reader()
        temp_list = [high_score,winner]
        if winner == scan_winner(temp_list):
            is_high_score = True
    
    if is_high_score:
        
        print ("New Top Card Updated !!".center(CENTER))
        with open(FILE_NAME,"wb") as f:
            pickle.dump(winner,f)

def high_score_remover():
    with open(FILE_NAME,"wb") as f:
        pass
    _ = input("Top Card Removed Successfully !!".center(CENTER))

def high_score_reader():
    if os.path.getsize(FILE_NAME) == 0:
        return None
    
    else:
        with open (FILE_NAME,"rb") as f:
            high_score = pickle.load(f)
        return high_score

def total_stats_reader():
    
    if os.path.getsize(FILE_NAME_2) == 0:
        default_list = [[0],[0,0,0,0,0,0]]
        with open (FILE_NAME_2,"w",newline="") as f:
            f_writer = csv.writer(f)
            f_writer.writerows(default_list)
    
    with open (FILE_NAME_2,"r") as f:
        f_reader = csv.reader(f)
        counter_list = list(f_reader)
        return counter_list

def total_stats_updater(hands_card_type):

    counter_list = total_stats_reader()
    counter_list[0][0] = int(counter_list[0][0])+1
    for index in range(0,6):
        if index == hands_card_type:
            counter_list[1][index] = int(counter_list[1][index]) + 1

    with open (FILE_NAME_2,"w",newline="") as f:
        f_writer = csv.writer(f)
        f_writer.writerows(counter_list)

def total_stats_remover():
    with open(FILE_NAME_2,"w",newline=""):
        pass
    _ = input("Stats Counter Removed Successfully !!".center(CENTER))


# CLASSES

class UI:

    def __init__(self):
        self.main_menu()
                
    def setup_game(self):
        
                title()
                players=[]
                while True:
                    user_choice = input("Enter Number of players [2-17]: ")
                    if any(user_choice == str(num) for num in range(2,18)):
                        number = int(user_choice)
                        break
                    else:
                        invalid()
                
                print()
                print("Enter Player Names:\n(Skip for Default Name)\n")
                for i in range(number):
                    temp_name = input(f"Player {i+1}: ")
                    if temp_name == "":
                        temp_name = f"Player {i+1}"
                    
                    players.append(Player(temp_name.title()))

                print ("Game Setup Completed !!".center(CENTER),end="")
                
                _ = input()
                return players

    def play_game(self, players):
        title()
        deck = Deck()
        deck.shuffle()
        for player in players:
            
            gap()
            player.hand_cards=[]
            player.draw_cards(deck)
            player.show_hand()
            print()
            print (f"Card Type: {card_type_dict[player.hand_cards_type()]}")
            print("\n")
            total_stats_updater(player.hand_cards_type())
        
        gap()
        winner = scan_winner(players)
        print(f"{winner.name} won with {card_type_dict[winner.hand_cards_type()]}".center(CENTER))
        gap()
        return winner

    def game_stats(self, high_score):
        title()
        
        if os.path.getsize(FILE_NAME) == 0:
            print("No Top Card Saved !!".center(CENTER))       
        else:
            print("Top Card: ")
            for card in high_score.hand_cards:
                card.show()
            print()
            print (f"Card Type: {card_type_dict[high_score.hand_cards_type()]}")

        counter_list = total_stats_reader()
        temp_header = "TOTAL DRAWS FROM DECK"
        total = counter_list[0][0]
        if int(total)==0:
            temp_percentage=0
        else:
            temp_percentage=round((1/1)*100,2)

        print()
        print("GAME STATS COUNTER".center(CENTER))
        print("\n")
        print (f"{temp_header:{COLUMN_SPACES}}: {total:{PERCENTAGE_SPACES}} [{str(temp_percentage):{6}}%]")
        for i in range(6):
            if int(counter_list[1][i]) != 0 and int(total) != 0:
                temp_percentage = round((int(counter_list[1][i])/int(total))*100,2)
            else:
                temp_percentage = round(0,2)
            print(f"{card_type_dict[i]:{COLUMN_SPACES}}: {counter_list[1][i]:{PERCENTAGE_SPACES}} [{str(temp_percentage):{6}}%]")

        print()
        user_choice = input()
        if user_choice == "reset stats":
            total_stats_remover()
        elif user_choice == "reset top card":
            high_score_remover()
        
    def exit(self):
        title()
        print("Thank You !!".center(CENTER),end="")
        _ = input()
        exit()
               
    def main_menu(self):
           
        players = []
        while True:
            title()
            print ('''
            1. Setup Game
            2. Play Game
            3. Game Stats
            4. Exit
            ''')
            
            print()
            while True:
                user_input = input("Enter your choice: ")
                if any((user_input) == str(num) for num in [1,2,3,4]):
                    valid_input = int(user_input)
                    break
                else:
                    invalid()

            if valid_input == 1:
                
                if len(players)==0:
                    players = self.setup_game()
                else:
                    title()
                    print ("Overwrite previous Game Setup?\nPress 'y' for yes,\nPress 'Enter' to go back.")
                    choice = input().lower()
                    if choice != "y":
                        pass
                    else:
                        players = self.setup_game()              
                
            elif valid_input == 2:
                
                if len(players)==0:
                    title()
                    print("Setup the Game First !!".center(CENTER),end="")
                    _=input()
                else:
                    while True:
                        winner = self.play_game(players)
                        high_score_updater(winner)
                        if not play_again():
                            break
                    
            elif valid_input == 3:
                high_score = high_score_reader()
                self.game_stats(high_score)
            
            elif valid_input == 4:
                self.exit()


class Card:

    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank

    def show(self):
        print (f"[{self.rank:2s} {self.suit}]",end="\t")

    def value(self):
        if any(self.rank == str(i) for i in range(2,11)):
            return int(self.rank)
        else:
            return ["J","Q","K","A"].index(self.rank) + 11


class Deck:

    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for suit in suit_list:
            for rank in rank_list:
                self.cards.append(Card(suit,rank))

    def show_deck(self):
        for card in self.cards:
            card.show()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()

    
class Player:

    def __init__ (self,name):
        self.hand_cards = []
        self.name = name

    def draw_cards(self,deck):
        for i in range(3):
            card = deck.draw_card()
            self.hand_cards.append(card)

    def show_hand(self):
        print(f"{self.name}: ".title())
        for card in self.hand_cards:
            card.show()

    def hand_dist(self):
        dict = {i:0 for i in range(1,15)}
        
        for card in self.hand_cards:
            dict[card.value()] += 1
        
        dict[1]=dict[14]
        return dict

    def hand_cards_type(self):

        dict = self.hand_dist()
        

        if isTrial(dict):
            return 5
        elif isStraight(dict) and isFlush(self):
            return 4
        elif isStraight(dict):
            return 3
        elif isFlush(self):
            return 2
        elif isPair(dict):
            return 1
        else:
            return 0

    def hand_cards_value(self):

        dict = self.hand_dist()

        if self.hand_cards_type() == 5:
            for i in range(2,15):
                if dict[i]==3:
                    return i

        elif any(self.hand_cards_type() == k for k in [4,3]):
            if all (dict[k] == 1 for k in [1,2,3]):
                return 14
            elif all (dict[k] == 1 for k in [12,13,14]):
                return 15
            
            for i in range(4,14):
                if all (dict[k] == 1 for k in [i,i-1,i-2]):
                    return i

        elif any(self.hand_cards_type() == k for k in [0,2]):
            for i in range(2,15):
                if dict[i]==1:
                    s=i
                    for j in range(i+1,15):
                        if dict[j]==1:
                            s=s+(j*100)
                            for k in range(j+1,15):
                                if dict[k]==1:
                                    s=s+(k*10000)
                                    return s

        elif self.hand_cards_type() == 1:           
            s = 0
            for i in range(2,15):
                if dict[i] == 1:
                    s = i
            for i in range(2,15):
                if dict[i] == 2:
                    s = s + (i*100)
                    return s



# MAIN FUNCTION

def main():
    
    ui = UI()

    

# EXECUTION

if __name__ == "__main__":
    main()

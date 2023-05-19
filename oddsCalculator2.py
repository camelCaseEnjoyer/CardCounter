import random as rand
import math

SUITS = ["H", "D", "S", "C"]

class Card:
    def __init__(self, rank, suit):
        if rank < 1 or rank > 13:
            raise IndexError("Given rankue" "is out of bounds.")
        if suit not in SUITS:
            raise rankueError("Given suit is inrankid")
        self.rank = rank
        self.suit = suit
    def name(self):
        name = ""
        if self.rank in range(2, 11):
            name += str(self.rank)
        elif self.rank == 1:
            name += "Ace"
        elif self.rank == 11:
            name += "Jack"
        elif self.rank == 12:
            name += "Queen"
        elif self.rank == 13:
            name += "King"
        
        if self.suit == "H":
           name += " of Hearts"
        elif self.suit == "D":
           name += " of Diamonds"
        elif self.suit == "C":
           name += " of Clubs"
        elif self.suit == "S":
           name += " of Spades"

        return name

    def __lt__(self, other):
        if self.suit == other.suit:
            return self.rank < other.rank
        else:
            return SUITS.index(self.suit) < SUITS.index(other.suit)

# Never ever let dupes in. Shit will break if there are dupes. 
class Deck:
    def __init__(self):
        self.reset()

    def reset(self):
        self.cards = []
        for s in SUITS:
            for i in range(1, 14):
                self.cards.append(Card(i, s))

    def remove(self, badCard):
        for card in self.cards:
            if badCard.rank == card.rank and card.suit == badCard.suit:
                self.cards.remove(card)
                return

    def empty(self):
        self.cards = []

    def insert(self, card):
        if card not in self.cards:
            self.cards.append(card)

    def copy(self):
        newDeck = Deck();
        newDeck.cards = self.cards.copy()
        return newDeck

    def sort(self):
        self.cards.sort()
                
    def compileStats(self):
        # 0 - Royal Flush
        # 1 - Straight Flush
        # 2 - Four of a Kind
        # 3 - Full House
        # 4 - Flush
        # 5 - Straight
        # 6 - Three of a kind
        # 7 - Two Pair
        # 8 - Pair
        allHands = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        royalDict = {
            "H" : 0,
            "D" : 0,
            "S" : 0,
            "C" : 0
        }
        rankDict = {
            1 : 0, 2 : 0, 3 : 0,
            4 : 0, 5 : 0, 6 : 0,
            7 : 0, 8 : 0, 9 : 0,
            10 : 0, 11 : 0, 12 : 0,
            13 : 0
        }
        suitDict = {
            "H" : 0,
            "D" : 0,
            "S" : 0,
            "C" : 0
        }
        sortedCards = sorted(self.cards)
        lastSuit = sortedCards[0].suit
        lastrank = sortedCards[0].rank
        cardsInARow = 0
        for card in sortedCards:
            if card.rank == 1 or card.rank >= 10:
                royalDict[card.suit] = royalDict[card.suit] + 1
            suitDict[card.suit] = suitDict[card.suit] + 1
            rankDict[card.rank] = rankDict[card.rank] + 1

            # straight flushes (not royal)
            if card.suit == lastSuit and card.rank == lastrank + 1:
                cardsInARow = cardsInARow + 1
            else:
                cardsInARow = 1
            if cardsInARow >= 5:
                allHands[1] = allHands[1] + 1
            lastSuit = card.suit
            lastrank = card.rank

        # royal flushes
        for suit in royalDict:
            if royalDict[suit] == 5:
                allHands[0] = allHands[0] + 1

        # regular flushes
        for suit in suitDict:
            if suitDict[suit] >= 5:
                allHands[4] = allHands[4] + math.comb(suitDict[suit], 5)
                
        # non straight, non flush hands
        for rank in rankDict:
            # 4OAK
            if rankDict[rank] == 4:
                allHands[2] = allHands[2] + 1
            if rankDict[rank] >= 3:
                # full house check
                for rank2 in rankDict:
                    if rankDict[rank2] >= 2 and rank != rank2:
                        allHands[3] = allHands[3] + math.comb(rankDict[rank], 3) * math.comb(rankDict[rank2], 2)
                # regular 3oak check
                allHands[6] = allHands[6] + math.comb(rankDict[rank], 3) * math.comb(len(self.cards) - rankDict[rank], 2)
            # pair and two pair
            if rankDict[rank] >= 2:
                allHands[8] = allHands[8] + math.comb(rankDict[rank], 2) * math.comb(len(self.cards) - rankDict[rank], 3)
                for rank2 in rankDict:
                    if rankDict[rank2] >= 2 and rank != rank2:
                        allHands[7] = allHands[7] + math.comb(rankDict[rank], 2) * \
                                  math.comb(rankDict[rank2], 2) * \
                                  (len(self.cards) - rankDict[rank] - rankDict[rank2])

        # regular straights
        for i in range(5, 14):
            allHands[5] = allHands[5] + rankDict[i - 4]* rankDict[i - 3] * rankDict[i - 2] * rankDict[i - 1] * rankDict[i]

        # count the 10-A straight, don't count royal or straight flushes
        allHands[5] = allHands[5] + rankDict[10] * rankDict[11] * rankDict[12] * rankDict[13] * rankDict[1] - allHands[0] - allHands[1]

        # four of a kind allows one wildcard
        allHands[2] = allHands[2] * (len(self.cards) - 4)

        # flushes don't count straight flushes
        allHands[4] = allHands[4] - allHands[1] - allHands[0]

        # three of a kind should not count full house
        allHands[6] = allHands[6] - allHands[3]

        # pair should not count two pair or full house
        allHands[8] = allHands[8] - allHands[7] - allHands[3]

        # two pair (and also pair) do some double counting on this algorithm
        allHands[7] = allHands[7] // 2

        
            
        return allHands
    
    def numRoyalFlushes(self):
        royalDict = {
            "H" : 0,
            "D" : 0,
            "S" : 0,
            "C" : 0
        }
        for card in self.cards:
            if card.rank == 1 or card.rank >= 10:
                royalDict[card.suit] = royalDict[card.suit] + 1
        numRoyalFlushes = 0
        for key in royalDict:
            if royalDict[key] == 5:
                numRoyalFlushes = numRoyalFlushes + 1
        return numRoyalFlushes * math.comb(len(self.cards) - 5, 2)
            

    def numStraightFlushes(self): # excluding royals
        straightFlushes = 0
        orderedCards = sorted(self.cards)
        cardsInARow = 1
        lastSuit = orderedCards[0].suit
        lastrank = orderedCards[0].rank
        for i in range(1, len(orderedCards)):
            currCard = orderedCards[i]
            if currCard.suit == lastSuit and currCard.rank == lastrank + 1:
                cardsInARow = cardsInARow + 1
            else:
                cardsInARow = 1
            if cardsInARow >= 5:
                straightFlushes = straightFlushes + 1
            lastSuit = currCard.suit
            lastrank = currCard.rank
            
        return straightFlushes * math.comb(len(self.cards) - 6, 2)
    
    def numFoursOfAKind(self):
        rankDict = {
            1 : 0, 2 : 0, 3 : 0,
            4 : 0, 5 : 0, 6 : 0,
            7 : 0, 8 : 0, 9 : 0,
            10 : 0, 11 : 0, 12 : 0,
            13 : 0
        }
        for card in self.cards:
            rankDict[card.rank] = rankDict[card.rank] + 1
        numQuads = 0
        for rank in rankDict:
            if rankDict[rank] == 4:
                numQuads = numQuads + 1
                
        return numQuads * math.comb(len(self.cards) - 4, 3)

    def numFullHouses(self):
        rankDict = {
            1 : 0, 2 : 0, 3 : 0,
            4 : 0, 5 : 0, 6 : 0,
            7 : 0, 8 : 0, 9 : 0,
            10 : 0, 11 : 0, 12 : 0,
            13 : 0
        }
        for card in self.cards:
            rankDict[card.rank] = rankDict[card.rank] + 1
        fullHouses = 0
        for v1 in rankDict:
            if rankDict[v1] >= 3:
                for v2 in rankDict:
                    if rankDict[v2] >= 2 and v1 > v2:
                        # This one got complicated
                        # You can take any 3 cards of rank v1, and any 2 cards of rank v2, followed by 2 cards
                        # where 1 or 0 of them are from rank v2 and neither is from rank v1.
                        fullHouses = fullHouses + math.comb(rankDict[v1], 3) * math.comb(rankDict[v2], 2) * \
                                   ((rankDict[v2] - 2) * (len(self.cards) - rankDict[v1] - rankDict[v2]) + \
                                    math.comb(len(self.cards) - rankDict[v1] - rankDict[v2], 2))                
                    elif rankDict[v2] >= 2 and v1 < v2:
                        # Less complicated
                        # Any three cards from rank v1 and any 2 cards of rank v2,
                        # and 2 more cards not in either v1 or v2.
                        fullHouses = fullHouses + math.comb(rankDict[v1], 3) * math.comb(rankDict[v2], 2) * \
                                     math.comb(len(self.cards) - rankDict[v1] - rankDict[v2], 2)
                        
        return fullHouses  - 3473184

    def numFlushes(self):
        suitDict = {
            "H" : 0,
            "D" : 0,
            "S" : 0,
            "C" : 0
        } 
        for card in self.cards:
            suitDict[card.suit] = suitDict[card.suit] + 1
        flushes = 0
        for suit in suitDict:
            if suitDict[suit] >= 5:
                flushes = flushes + math.comb(suitDict[suit], 5)
        return flushes - self.numStraightFlushes() - self.numRoyalFlushes()
    
    def numStraights(self):
        rankDict = {
            1 : 0, 2 : 0, 3 : 0,
            4 : 0, 5 : 0, 6 : 0,
            7 : 0, 8 : 0, 9 : 0,
            10 : 0, 11 : 0, 12 : 0,
            13 : 0
        }
        straights = 0
        for card in self.cards:
            rankDict[card.rank] = rankDict[card.rank] + 1
        for i in range(5, 14):
            straights = straights + rankDict[i - 4] * rankDict[i - 3] * \
                        rankDict[i - 2] * rankDict[i - 1] * rankDict[i]
        straights = straights + rankDict[10] * rankDict[11] * rankDict[12]\
                    * rankDict[13] * rankDict[1]    
                    
        return straights - self.numStraightFlushes() - self.numRoyalFlushes()
    
    def numThreesOfAKind(self):
        rankDict = {
            1 : 0, 2 : 0, 3 : 0,
            4 : 0, 5 : 0, 6 : 0,
            7 : 0, 8 : 0, 9 : 0,
            10 : 0, 11 : 0, 12 : 0,
            13 : 0
        }
        trips = 0
        for card in self.cards:
            rankDict[card.rank] = rankDict[card.rank] + 1
        for key in rankDict:
            if rankDict[key] >= 3:
                trips = trips + math.comb(rankDict[key], 3) * math.comb(len(self.cards) - rankDict[key], 2)
        return trips - self.numFullHouses()
    
    def numTwoPairs(self):
        rankDict = {
            1 : 0, 2 : 0, 3 : 0,
            4 : 0, 5 : 0, 6 : 0,
            7 : 0, 8 : 0, 9 : 0,
            10 : 0, 11 : 0, 12 : 0,
            13 : 0
        }
        dubdubs = 0
        for card in self.cards:
            rankDict[card.rank] = rankDict[card.rank] + 1
        for k1 in rankDict:
            if rankDict[k1] >= 2:
                for k2 in rankDict:
                    if rankDict[k2] >= 2 and k1 != k2:
                        dubdubs = dubdubs + math.comb(rankDict[k1], 2) * \
                                  math.comb(rankDict[k2], 2) * \
                                  (len(self.cards) - rankDict[k1] - rankDict[k2])
        return dubdubs // 2 # nested for loop counts (k1, k2) and (k2, k1)
    def numPairs(self):
        rankDict = {
            1 : 0, 2 : 0, 3 : 0,
            4 : 0, 5 : 0, 6 : 0,
            7 : 0, 8 : 0, 9 : 0,
            10 : 0, 11 : 0, 12 : 0,
            13 : 0
        }
        dubs = 0
        for card in self.cards:
            rankDict[card.rank] = rankDict[card.rank] + 1
        for k1 in rankDict:
            if rankDict[k1] >= 2:
                dubs = dubs + math.comb(rankDict[k1], 2) * math.comb(len(self.cards) - rankDict[k1], 3)
        return dubs - 2* self.numTwoPairs() - self.numFullHouses()
    
            
deck = Deck()
rand.shuffle(deck.cards)
for card in deck.cards:
    print(card.name())
stats = deck.compileStats()
print ("There are", stats[0], "royal flushes.")
print ("There are", stats[1], "straight flushes.")
print ("There are", stats[2], "fours of a kind.")
print ("There are", stats[3], "full houses.")
print ("There are", stats[4], "regular flushes.")
print ("There are", stats[5], "regular straights.")
print ("There are", stats[6], "threes of a kind.")
print ("There are", stats[7], "two pairs.")
print ("There are", stats[8], "pairs.")
deck.sort()
print ("There are", deck.numRoyalFlushes(), "royal flushes with 7 card hands.")
print ("There are", deck.numStraightFlushes() , "straight flushes with 7 card hands.")
print ("There are", deck.numFoursOfAKind(), "fours of a kind with 7 card hands.")
print ("There are", deck.numFullHouses(), "full houses with 7 card hands.")
print ("There are", deck.numFlushes(), "regular flushes with 7 card hands.")
print ("There are", deck.numStraights(), "regular straights with 7 card hands.")
print ("There are", deck.numThreesOfAKind(), "threes of a kind with 7 card hands.")
print ("There are", deck.numTwoPairs(), "two pairs with 7 card hands.")
print ("There are", deck.numPairs(), "pairs with 7 card hands.")




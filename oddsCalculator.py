import random as rand
import math

SUITS = ["H", "D", "S", "C"]

class Card:
    def __init__(self, val, suit):
        if val < 1 or val > 13:
            raise IndexError("Given value" "is out of bounds.")
        if suit not in SUITS:
            raise ValueError("Given suit is invalid")
        self.val = val
        self.suit = suit
    def name(self):
        name = ""
        if self.val in range(2, 11):
            name += str(self.val)
        elif self.val == 1:
            name += "Ace"
        elif self.val == 11:
            name += "Jack"
        elif self.val == 12:
            name += "Queen"
        elif self.val == 13:
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
            return self.val < other.val
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
            if badCard.val == card.val and card.suit == badCard.suit:
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
        valDict = {
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
        lastVal = sortedCards[0].val
        cardsInARow = 0
        for card in sortedCards:
            if card.val == 1 or card.val >= 10:
                royalDict[card.suit] = royalDict[card.suit] + 1
            suitDict[card.suit] = suitDict[card.suit] + 1
            valDict[card.val] = valDict[card.val] + 1

            # straight flushes (not royal)
            if card.suit == lastSuit and card.val == lastVal + 1:
                cardsInARow = cardsInARow + 1
            else:
                cardsInARow = 1
            if cardsInARow >= 5:
                allHands[1] = allHands[1] + 1
            lastSuit = card.suit
            lastVal = card.val

        # royal flushes
        for suit in royalDict:
            if royalDict[suit] == 5:
                allHands[0] = allHands[0] + 1

        # regular flushes
        for suit in suitDict:
            if suitDict[suit] >= 5:
                allHands[4] = allHands[4] + math.comb(suitDict[suit], 5)
                
        # non straight, non flush hands
        for val in valDict:
            # 4OAK
            if valDict[val] == 4:
                allHands[2] = allHands[2] + 1
            if valDict[val] >= 3:
                # full house check
                for val2 in valDict:
                    if valDict[val2] >= 2 and val != val2:
                        allHands[3] = allHands[3] + math.comb(valDict[val], 3) * math.comb(valDict[val2], 2)
                # regular 3oak check
                allHands[6] = allHands[6] + math.comb(valDict[val], 3) * math.comb(len(self.cards) - valDict[val], 2)
            # pair and two pair
            if valDict[val] >= 2:
                allHands[8] = allHands[8] + math.comb(valDict[val], 2) * math.comb(len(self.cards) - valDict[val], 3)
                for val2 in valDict:
                    if valDict[val2] >= 2 and val != val2:
                        allHands[7] = allHands[7] + math.comb(valDict[val], 2) * \
                                  math.comb(valDict[val2], 2) * \
                                  (len(self.cards) - valDict[val] - valDict[val2])

        # regular straights
        for i in range(5, 14):
            allHands[5] = allHands[5] + valDict[i - 4]* valDict[i - 3] * valDict[i - 2] * valDict[i - 1] * valDict[i]

        # count the 10-A straight, don't count royal or straight flushes
        allHands[5] = allHands[5] + valDict[10] * valDict[11] * valDict[12] * valDict[13] * valDict[1] - allHands[0] - allHands[1]

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
            if card.val == 1 or card.val >= 10:
                royalDict[card.suit] = royalDict[card.suit] + 1
        numRoyalFlushes = 0
        for key in royalDict:
            if royalDict[key] == 5:
                numRoyalFlushes = numRoyalFlushes + 1
        return numRoyalFlushes
            

    def numStraightFlushes(self): # excluding royals
        straightFlushes = 0
        orderedCards = sorted(self.cards)
        cardsInARow = 1
        lastSuit = orderedCards[0].suit
        lastVal = orderedCards[0].val
        for i in range(1, len(orderedCards)):
            currCard = orderedCards[i]
            if currCard.suit == lastSuit and currCard.val == lastVal + 1:
                cardsInARow = cardsInARow + 1
            else:
                cardsInARow = 1
            if cardsInARow >= 5:
                straightFlushes = straightFlushes + 1
            lastSuit = currCard.suit
            lastVal = currCard.val
            
        return straightFlushes
    
    def numFoursOfAKind(self):
        valDict = {
            1 : 0, 2 : 0, 3 : 0,
            4 : 0, 5 : 0, 6 : 0,
            7 : 0, 8 : 0, 9 : 0,
            10 : 0, 11 : 0, 12 : 0,
            13 : 0
        }
        for card in self.cards:
            valDict[card.val] = valDict[card.val] + 1
        numQuads = 0
        for val in valDict:
            if valDict[val] == 4:
                numQuads = numQuads + 1
                
        return numQuads * (len(self.cards) - 4)

    def numFullHouses(self):
        valDict = {
            1 : 0, 2 : 0, 3 : 0,
            4 : 0, 5 : 0, 6 : 0,
            7 : 0, 8 : 0, 9 : 0,
            10 : 0, 11 : 0, 12 : 0,
            13 : 0
        }
        for card in self.cards:
            valDict[card.val] = valDict[card.val] + 1
        fullHouses = 0
        for v1 in valDict:
            if valDict[v1] >= 3:
                for v2 in valDict:
                    if valDict[v2] >= 2 and v1 != v2:
                      fullHouses = fullHouses + math.comb(valDict[v1], 3) * math.comb(valDict[v2], 2)  
        return fullHouses

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
        valDict = {
            1 : 0, 2 : 0, 3 : 0,
            4 : 0, 5 : 0, 6 : 0,
            7 : 0, 8 : 0, 9 : 0,
            10 : 0, 11 : 0, 12 : 0,
            13 : 0
        }
        straights = 0
        for card in self.cards:
            valDict[card.val] = valDict[card.val] + 1
        for i in range(5, 14):
            straights = straights + valDict[i - 4] * valDict[i - 3] * \
                        valDict[i - 2] * valDict[i - 1] * valDict[i]
        straights = straights + valDict[10] * valDict[11] * valDict[12]\
                    * valDict[13] * valDict[1]    
                    
        return straights - self.numStraightFlushes() - self.numRoyalFlushes()
    def numThreesOfAKind(self):
        valDict = {
            1 : 0, 2 : 0, 3 : 0,
            4 : 0, 5 : 0, 6 : 0,
            7 : 0, 8 : 0, 9 : 0,
            10 : 0, 11 : 0, 12 : 0,
            13 : 0
        }
        trips = 0
        for card in self.cards:
            valDict[card.val] = valDict[card.val] + 1
        for key in valDict:
            if valDict[key] >= 3:
                trips = trips + math.comb(valDict[key], 3) * math.comb(len(self.cards) - valDict[key], 2)
        return trips - self.numFullHouses()
    
    def numTwoPairs(self):
        valDict = {
            1 : 0, 2 : 0, 3 : 0,
            4 : 0, 5 : 0, 6 : 0,
            7 : 0, 8 : 0, 9 : 0,
            10 : 0, 11 : 0, 12 : 0,
            13 : 0
        }
        dubdubs = 0
        for card in self.cards:
            valDict[card.val] = valDict[card.val] + 1
        for k1 in valDict:
            if valDict[k1] >= 2:
                for k2 in valDict:
                    if valDict[k2] >= 2 and k1 != k2:
                        dubdubs = dubdubs + math.comb(valDict[k1], 2) * \
                                  math.comb(valDict[k2], 2) * \
                                  (len(self.cards) - valDict[k1] - valDict[k2])
        return dubdubs // 2 # nested for loop counts (k1, k2) and (k2, k1)
    def numPairs(self):
        valDict = {
            1 : 0, 2 : 0, 3 : 0,
            4 : 0, 5 : 0, 6 : 0,
            7 : 0, 8 : 0, 9 : 0,
            10 : 0, 11 : 0, 12 : 0,
            13 : 0
        }
        dubs = 0
        for card in self.cards:
            valDict[card.val] = valDict[card.val] + 1
        for k1 in valDict:
            if valDict[k1] >= 2:
                dubs = dubs + math.comb(valDict[k1], 2) * math.comb(len(self.cards) - valDict[k1], 3)
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





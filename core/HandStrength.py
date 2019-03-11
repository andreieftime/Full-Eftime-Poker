from enums.Number import Number

#we will have separate functions to check for each poker combination
def checkFlush(cards):
    suit = cards[0].suit

    for card in cards:
        if card.suit != suit:
            return 0

    return 1

def checkStraight(cards):
    numbers = [0 for i in range(14)]

    for card in cards:
        x = card.number
        if x==0:
            numbers[0] += 1
            numbers[13] += 1
        else:
            numbers[x] += 1

    #we will count how many consecutive cards we have
    consecutive = 0
    for i in numbers:
        if i!=0:
            consecutive += 1
        else:
            consecutive = 0

        if consecutive==5:
            return 1

    return 0

def checkStraightFlush(cards):
    if checkStraight(cards)==1 and checkFlush(cards)==1:
        return 1
    else:
        return 0

def checkQuads(cards):
    numbers = [0 for i in range(13)]

    for card in cards:
        numbers[card.number] += 1

        if numbers[card.number]==4:
            return 1
    return 0

def checkFull(cards):
    numbers = [0 for i in range(13)]

    for card in cards:
        numbers[card.number] += 1

    we_have_3 = 0
    we_have_2 = 0
    for i in numbers:
        if i==3:
            we_have_3 = 1
        if i==2:
            we_have_2 = 1

    if we_have_2==1 and we_have_3==1:
        return 1
    else:
        return 0

def checkTrips(cards):
    numbers = [0 for i in range(13)]

    for card in cards:
        numbers[card.number] += 1

        if numbers[card.number] == 3:
            return 1
    return 0

def check2Pair(cards):
    numbers = [0 for i in range(13)]

    for card in cards:
        numbers[card.number] += 1

    number_2 = 0
    for i in numbers:
        if i == 2:
            number_2 += 1

    if number_2==2:
        return 1
    else:
        return 0

def checkPair(cards):
    numbers = [0 for i in range(13)]

    for card in cards:
        numbers[card.number] += 1

    number_2 = 0
    for i in numbers:
        if i == 2:
            number_2 += 1

    if number_2 == 1:
        return 1
    else:
        return 0


# this function will return how good a hand is
# it will return the combination (straight, flush, two pair etc)
# and something about the combination
def Strength(cards):
    #Check for Straight flush
    if checkStraightFlush(cards)==1:
        return 8
    if checkQuads(cards)==1:
        return 7
    if checkFull(cards)==1:
        return 6
    if checkFlush(cards)==1:
        return 5
    if checkStraight(cards)==1:
        return 4
    if checkTrips(cards)==1:
        return 3
    if check2Pair(cards)==1:
        return 2
    if checkPair(cards)==1:
        return 1

    return 0

#for each combination we will have function that compares
#hands with these combinations in order to decide who is better
def analyseStraightFlush(cards):
    numbers = [0 for i in range(14)]

    for card in cards:
        x = card.number

        if x==0:
            numbers[0] += 1
            numbers[13] += 1
        else:
            numbers[x] += 1

    consecutive = 0
    for i in range(14):
        if numbers[i]==1:
            consecutive += 1
        else:
            consecutive = 0

        if consecutive==5:
            return i

    return -1

def analyseQuads(cards):
    numbers = [0 for i in range(13)]

    q = 0
    kick = 0
    for card in cards:
        if card.number==0:
            numbers[12] += 1
        else:
            numbers[card.number - 1] += 1
    for i in range(len(numbers)):
        if numbers[i]==4:
            q = i
        if numbers[i]==1:
            kick = i
    return q, kick

def analyseFull(cards):
    numbers = [0 for i in range(13)]

    Value3 = 0
    Value2 = 0
    for card in cards:
        if card.number == 0:
            numbers[12] += 1
        else:
            numbers[card.number - 1] += 1
    for i in range(len(numbers)):
        if numbers[i] == 3:
            Value3 = i
        if numbers[i] == 2:
            Value2 = i

    return Value3, Value2

def analyseFlush(cards):
    numbers = [0 for i in range(13)]

    for card in cards:
        if card.number  == 0:
            numbers[12] += 1
        else:
            numbers[card.number - 1] += 1

    return numbers

def analyseStraight(cards):
    numbers = [0 for i in range(14)]

    for card in cards:
        x = card.number

        if x == 0:
            numbers[0] += 1
            numbers[13] += 1
        else:
            numbers[x] += 1

    consecutive = 0
    for i in range(14):
        if numbers[i] == 1:
            consecutive += 1
        else:
            consecutive = 0

        if consecutive == 5:
            return i

    return -1

def analyseTrips(cards):
    numbers = [0 for i in range(13)]

    for card in cards:
        if card.number  == 0:
            numbers[12] += 1
        else:
            numbers[card.number  - 1] += 1

    trip = 0
    kick1 = 0
    kick2 = 0
    for i in range(13):
        if numbers[i]==3:
            trip = i
        if numbers[i]==1:
            kick2 = kick1
            kick1 = i

    return trip, kick1, kick2

def analyse2Pair(cards):
    numbers = [0 for i in range(13)]

    for card in cards:
        if card.number  == 0:
            numbers[12] += 1
        else:
            numbers[card.number  - 1] += 1

    p1 = 0
    p2 = 0
    kick = 0
    for i in range(13):
        if numbers[i]==1:
            kick = i
        if numbers[i]==2:
            p2 = p1
            p1 = i

    return p1, p2, kick

def analysePair(cards):
    numbers = [0 for i in range(13)]

    for card in cards:
        if card.number  == 0:
            numbers[12] += 1
        else:
            numbers[card.number  - 1] += 1

    p = 0
    for i in range(13):
        if numbers[i]==2:
            numbers[i] = 0
            p = i

    return p, numbers

def analyseHighCard(cards):
    numbers = [0 for i in range(13)]

    for card in cards:
        if card.number  == 0:
            numbers[12] += 1
        else:
            numbers[card.number  - 1] += 1

    return numbers

def HandCompare(cards1, cards2):
    if Strength(cards1)>Strength(cards2):
        return 1
    if Strength(cards1)<Strength(cards2):
        return 0
    if Strength(cards1)==Strength(cards2):
        if Strength(cards1)==8:
            if analyseStraightFlush(cards1)>analyseStraightFlush(cards2):
                return 1
            if analyseStraightFlush(cards1)<analyseStraightFlush(cards2):
                return 0
            if analyseStraightFlush(cards1)==analyseStraightFlush(cards2):
                return -1

        if Strength(cards1)==7:
            q1, kick1 = analyseQuads(cards1)
            q2, kick2 = analyseQuads(cards2)

            if q1>q2:
                return 1
            if q1<q2:
                return 0
            if q1==q2:
                if kick1>kick2:
                    return 1
                if kick1<kick2:
                    return 0
                if kick1==kick2:
                    return -1

        if Strength(cards1)==6:
            t1, d1 = analyseFull(cards1)
            t2, d2 = analyseFull(cards2)

            if t1 > t2:
                return 1
            if t1 < t2:
                return 0
            if t1 == t2:
                if d1 > d2:
                    return 1
                if d1 < d2:
                    return 0
                if d1 == d2:
                    return -1

        if Strength(cards1)==5:
            poz1 = analyseFlush(cards1)
            poz2 = analyseFlush(cards2)

            verify = 0
            for i in range(13):
                if poz1[12 - i]==1 and poz2[12 - i]==0:
                    verify = 1
                    return 1
                if poz2[12 - i]==1 and poz1[12 - i]==0:
                    verify = 1
                    return 0

            if verify==0:
                return -1

        if Strength(cards1)==4:
            if analyseStraight(cards1)>analyseStraight(cards2):
                return 1
            if analyseStraight(cards1)<analyseStraight(cards2):
                return 0
            if analyseStraight(cards1)==analyseStraight(cards2):
                return -1

        if Strength(cards1)==3:
            poz1 = analyseTrips(cards1)
            poz2 = analyseTrips(cards2)

            verify = 0
            for i in range(3):
                if poz1[i]>poz2[i]:
                    verify = 1
                    return 1
                if poz1[i]<poz2[i]:
                    verify = 1
                    return 0

            if verify==0:
                return -1

        if Strength(cards1)==2:
            poz1 = analyse2Pair(cards1)
            poz2 = analyse2Pair(cards2)

            verify = 0
            for i in range(3):
                if poz1[i] > poz2[i]:
                    verify = 1
                    return 1
                if poz1[i] < poz2[i]:
                    verify = 1
                    return 0

            if verify == 0:
                return -1

        if Strength(cards1)==1:
            p1, poz1 = analysePair(cards1)
            p2, poz2 = analysePair(cards2)

            if p1>p2:
                return 1
            if p1<p2:
                return 0
            if p1==p2:
                verify = 0
                for i in range(13):
                    if int(poz1[12 - i]) == 1 and poz2[12 - i] == 0:
                        verify = 1
                        return 1
                    if poz2[12 - i] == 1 and poz1[12 - i] == 0:
                        verify = 1
                        return 0

                if verify == 0:
                    return -1

        if Strength(cards1)==0:
            poz1 = analyseHighCard(cards1)
            poz2 = analyseHighCard(cards2)

            verify = 0
            for i in range(13):
                if poz1[12 - i] == 1 and poz2[12 - i] == 0:
                    verify = 1
                    return 1
                if poz2[12 - i] == 1 and poz1[12 - i] == 0:
                    verify = 1
                    return 0

            if verify == 0:
                return -1

#this function will display each combination
def assess_hand(cards):
    if Strength(cards)==8:
        x = analyseStraightFlush(cards)
        return "You have a Straight Flush " + Number(x).name + " high"
    if Strength(cards)==7:
        x, y = analyseQuads(cards)
        return "You have four of a kind " + Number(x + 1).name
    if Strength(cards)==6:
        x, y = analyseFull(cards)
        return "You have a Full House " + Number(x + 1).name + "s with " + Number(y + 1).name + "s"
    if Strength(cards)==5:
        poz = analyseFlush(cards)
        for i in range(13):
            if poz[12 - i]!=0:
                return "You have a Flush " + Number(12 - i + 1).name + " high"
    if Strength(cards)==4:
        x = analyseStraight(cards)
        return "You have a Straight " + Number(x).name + " high"
    if Strength(cards)==3:
        x, y, z = analyseTrips(cards)
        return "You have three o a kind " + Number(x + 1).name + "s"
    if Strength(cards)==2:
        x,y, z = analyse2Pair(cards)
        return "You have two pairs " + Number(x + 1).name + "s" + " and " + Number(y + 1).name + "s"
    if Strength(cards)==1:
        x, y = analysePair(cards)
        return "You have a pair of " + Number(x + 1).name + "s"
    if Strength(cards)==0:
        poz = analyseHighCard(cards)
        for i in range(13):
            if poz[12 - i] != 0:
                return "You have a High Card " + Number(12 - i + 1).name + " high"

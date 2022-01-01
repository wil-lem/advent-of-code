
from enum import unique
from os import stat
import re
import statistics

def part_one(p1pos,p2pos):
    game = Game()
    player1 = Player(p1pos)
    player2 = Player(p2pos)
    game.addPlayer(player1)
    game.addPlayer(player2)
    game.play() 
    
    loser = game.getLoser()
    print('P1 ' + str(game.die.count * loser.score))
    
def part_two(p1pos,p2pos):
    # Mapped out how many universes are created in 3 throws for specific numer of steps 
    stepsMap = [
        {'steps':3,'universes':1},
        {'steps':4,'universes':3},
        {'steps':5,'universes':6},
        {'steps':6,'universes':7},
        {'steps':7,'universes':6},
        {'steps':8,'universes':3},
        {'steps':9,'universes':1}
    ]

    # p1States = [{'pos':p1pos,'score':0, 'universes':0,'throws':0}]
    
    p1 = AdvanceDPlayer(p1pos,'Player 1')
    p2 = AdvanceDPlayer(p2pos,'Player 2')

    allWon = False
    currentPlayer = p1
    otherPlayer = p2

    while not allWon:
        currentPlayer.takeTurn(otherPlayer.getActiveUniverses())

        # Switch player
        if currentPlayer == p1:
            currentPlayer = p2
            otherPlayer = p1
        else: 
            currentPlayer = p1
            otherPlayer = p2

        if p1.getActiveUniverses() == 0 or p2.getActiveUniverses() == 0:
            allWon = True

    wins = max(p1.getWonUniverses(),p2.getWonUniverses())
    
    print('P2 ' + str(int(wins)))
    


class GameState():
    def __init__(self, pos, score, universes, throws):
        self.pos = pos
        self.score = score
        self.universes = universes
        self.throws = throws

    def __str__(self) -> str:
        return 't:' + str(self.throws) + ' p: ' + str(self.pos) + ' s: ' + str(self.score) + ' u: ' + str(self.universes)
    
    def matches(self,otherState):
        if self.throws == otherState.throws and self.pos == otherState.pos and self.score == otherState.score:
                return True
        return False

    def mergeWithState(self,other):
        self.universes += other.universes

    def isWon(self):
        # return self.score >= 4
        return self.score >= 21

class AdvanceDPlayer():
    def __init__(self,pos,name):
        startState = GameState(pos,0,1,0)
        self.states = [startState]
        self.name = name
    
    def takeTurn(self, startUniverses):

        # say p1 has had one turn, that means there are 27 universes
        # Whatever player 2 does, it will happen in 27 universes so we need to add this to the generated univeses

        # We know what will happen if we throw the dice 3 times, it's mapped out below
        # steps: the number of steps the player can move
        # universes: the number of universes this happens in.
        stepsMap = [
            {'steps':3,'universes':1},
            {'steps':4,'universes':3},
            {'steps':5,'universes':6},
            {'steps':6,'universes':7},
            {'steps':7,'universes':6},
            {'steps':8,'universes':3},
            {'steps':9,'universes':1}
        ]

        # stepsMap = [
        #     {'steps':2,'universes':1},
        #     {'steps':3,'universes':2},
        #     {'steps':4,'universes':1},
        # ]

        states = []
        activeCount = self.getActiveUniverses()
        for startState in self.states:
            if startState.isWon():
                states.append(startState)
                continue 
            
            for mappedStep in stepsMap:
                pos = (startState.pos + mappedStep['steps']) % 10
                if pos < 1:
                    pos += 10
                
                universes = startUniverses * mappedStep['universes'] * startState.universes/activeCount
                score = startState.score + pos
                newState = GameState(pos, score, universes, startState.throws + 3)
        
                states.append(newState)
        
        self.states = states

        self.cleanStates()

        self.states.sort(key=lambda s: s.score)
    
    def printStates(self):
        for state in self.states:
            print(str(state))
        print()
    
    def calculateuniverses(self):
        for s in self.states:
            print(self.states)

    def addUniverses(self,count):
        for state in list(filter(lambda s: not s.isWon(),self.states)):
            state.universes += count 
        

    def cleanStates(self):
        states = []
        for oldState in self.states:
            similar = list(filter(lambda otherState: otherState.matches(oldState),states))
            if len(similar) == 1:
                similar[0].mergeWithState(oldState)
            else:
                states.append(oldState)
            
        self.states = states

    def getActiveUniverses(self):
        u = 0
        for s in self.states:
            if not s.isWon():
                u+= s.universes
        return u

    def getWonUniverses(self):
        u = 0
        for s in self.states:
            if s.isWon():
                u+= s.universes
        return u

            
    
class DeterministicDie:
    def __init__(self):
        self.next = 1
        self.count = 0
    
    def cast(self):       
        val = self.next
        
        self.count += 1
        self.next += 1

        if self.next > 100:
            self.next = 1
        return val

class Game:
    def __init__(self):
        self.playerTurnIndex = 0
        self.players = []
        self.die = DeterministicDie()
    
    def addPlayer(self,player):
        self.players.append(player)
    
    def play(self):
        
        done = False
        while not done:
            totalCast = 0 
            
            currentPlayer = self.getCurrentPlayer()
            descr = 'Player ' + str(self.players.index(currentPlayer)+1) + ' rolls '

            for i in range(0,3):
                val = self.die.cast()
                totalCast += val
                descr += str(val)
                if(i < 2):
                    descr += '+'
            
            
            currentPlayer.move(totalCast)

            descr += ' and moves to space ' + str(currentPlayer.pos) + ' for a total score of ' + str(currentPlayer.score)
            
            
            #print(descr)

            
            

            for player in self.players:
                if player.score >= 1000:
                    return
            
            self.nextTurn()

    def nextTurn(self):
        self.playerTurnIndex += 1
        if self.playerTurnIndex > len(self.players) - 1:
            self.playerTurnIndex = 0

    def getCurrentPlayer(self):
        return self.players[self.playerTurnIndex]

    def getLoser(self):
        players = self.players[:]
        players.sort(key=lambda p: p.score)
        return players[0]

class Player:
    def __init__(self,pos):
        self.score = 0
        self.pos = pos
    
    def move(self,count):
        self.pos += count
        self.pos = self.pos % 10
        if self.pos < 1:
            self.pos += 10
        self.score += self.pos

part_one(4,8)
part_one(3,5)
part_two(4,8)
part_two(3,5)

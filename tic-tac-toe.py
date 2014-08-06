#Programme: Tic Tac Toe.
#Status: To be implemented
# Levels: 1)Simple: random computer input 2) Hard: Computer never lose the game
#By dharmendra30@yahoo.com
#Date & Version: Aug 2014, 1.0
import sys
import random

#Global variables
CompSymbol=None
PlyerSymbol=None
Board = ['_']*9
NextMover = None #possible value: 'Computer, 'Player
MoveCount=0#max is 9 starting from 1
MovesMade=[]#stores already moves played. User for intelligence
NextMoveFromSM=False # to double threat when computer Player starts move with corner move. Here, Compuetr should make first move at central place and in next turn, it should move to side-middle place having opposite sid-middle also available.

#difficulty level
#Level='random' #smart
Level='smart'#in this mode computer will never lose!

def debug(str):
	pass
	#print(str)

#Helper function
#init/Reset
def init_game():
	global Board, CompSymbol, PlayerSymbol, NextMover, MoveCount, MovesMade, NextMoveFromSM
	Board = ['_']*9#zero index is in use
	MoveCount = 0
	MovesMade=[]
	NextMoveFromSM=False
	
	PlayerSymbol, CompSymbol = getPlayerSymbols()
	#select who will get first move
	if random.randint(0,1)==0:
		NextMover='Computer'
	else:
		NextMover='Player'

def getPlayerSymbols():
	print('Select Your Symbol[X, O]:')
	symbol = input().upper()
	if symbol=='X':
		return ['X', 'O'];#first is for player, second if for computer
	else:
		return ['O', 'X']

def print_board():
	global PlayerSymbol, CompSymbol, MoveCount, Board
	print('Player='+PlayerSymbol+', Computer='+CompSymbol + ' , Total moves=' + str(MoveCount))
	print(Board[0]+' | ' + Board[1] + ' | ' + Board[2] + '\n')
	print(Board[3]+' | ' + Board[4] + ' | ' + Board[5] + '\n')
	print(Board[6]+' | ' + Board[7] + ' | ' + Board[8] + '\n')

#returns true if player wins after this move, otherwise returns False
#def makeMove(board, player, move):
def makeMove(b, player, move):
	global Board, MoveCount, NextMover, MovesMade
	
	if move==None:
		return False
	if Board[move]==' ' or Board[move]=='_':
		Board[move]=player
		MoveCount+=1
		MovesMade.append(move)

		if NextMover=='Player':
			NextMover='Computer'
		else:
			print('\nComputer move was at:' +str(move+1))
			NextMover='Player'
		debug(Board)
		return isWinnerAfterMove(Board, player, move)
	else:
		print('makeMove:move is not possible')
		return False

def isWinnerAfterMove(b, player, move):#b=>board
	global Board, CompSymbol, PlayerSymbol, NextMover
	#local vars
	restore = b[move]=='_'#restore the empty char after test
	win=False
	
	if restore:
		b[move]=player
	#debug('in isWinnerA, b=:'+str(b))
	r=(move)//3#row using index 0
	c=move%3#column
	rbase=r*3#first index for selected row
	cbase=c#first index for selected row
	debug('move='+str(move)+ ' r=' + str(r) +' c='+str(c)+' rbase='+str(rbase) + ' cbase='+str(cbase))
	if (r==c or move==2 or move==6):#center. Check diagonals
		win=( (b[0] == b[4] == b[8]==player) or 
				(b[2]==b[4]==b[6]==player))
	if not win: #check row or column of move location
		win=( (b[rbase] == b[rbase+1] == b[rbase+2]==player) or
				(b[cbase]==b[cbase+3]==b[cbase+6]==player))
	if restore:
		b[move]='_'#reset the move location
	return win	

#random choice from available moves
def getMoveFromList(moves):
	global Board
	availableMoves=[]
	for i in moves:
		if Board[i]=='_':
			availableMoves.append(i)

	if len(availableMoves)!=0:
		#return availableMoves[0]#select first. It would be better to select one randomly
		return random.choice(availableMoves)#select randomly
	else:
		return None


def getPlayerMoveLocation():
	global Board
	move=-1
	#while (move <1 or move >9 or Board[move-1]!=' '):
	while (move <1 or move >9 or Board[move-1]!='_'):
		print('Your turn: Enter move location<1 to 9> and already not used>:')
		move=int(input())
	return move-1#based on zero index	

def getComputerMoveLocation():#current move is not completed yet
	global Board, CompSymbol, PlayerSymbol, NextMover, MovesMade, Level, NextMoveFromSM

	if Level=='random':
		#random
		return getMoveFromList([0,1,2,3,4,5,6,7,8])
	elif Level=='smart':#computer never loses
		debug('Using smart algo')
		#check move which make computer win
		for i in range(0, 8):
			if(Board[i]=='_' and isWinnerAfterMove(Board, CompSymbol, i)):
				return i
		#check move which makes player win. Block Player's win
		for i in range(0, 8):
			if(Board[i]=='_' and isWinnerAfterMove(Board, PlayerSymbol, i)):
				return i
	
		#avoid possible double threat, when player starts move with corner place
		#Computer will move at center and then in side-middle (having opposite side-middle also available for Player to fix his move.
		if NextMover=='Computer' and MoveCount==1: #this is first move of computer after opening move of Player
			debug('1st move by Player at corner. Computer follows with 2nd move at center')
			if MovesMade[0] in [0, 2, 6, 8]:#Player's start move is in corner
				NextMoveFromSM=True#SM: side middle
				return 4#return center move
		elif MoveCount==3 and NextMoveFromSM:##Player started move in corner, this is 2nd move o computer in side-middle
			NextMoveFromSM=False
			#Use side-middle moves [1, 3, 5, 7] to avoid double threats 
			#from side-middle and opposit side-middle should be available for next move
			if Board[1]=='_' and Board[7]=='_':#both places are available
				return 1;
			if Board[3]=='_' and Board[5]=='_':#both places are available
				return 3;
		#check if corner is available
		#try to fine best corner move with largest number of promising and contributing triplets
		availc=[]
		usedc=[]
		for m in [0,2,6,8]:
			if Board[m]=='_':
				availc.append(m)
			elif Board[m]==CompSymbol:
				usedc.append(m)
		max_score=0
		move=-1
		for c in availc:
			score=0
			for u in usedc:
				if Board[(c+u)//2]=='_':
					score+=1
			if (max_score<score):
				max_score=score
				move=c
		debug('Best corner:move='+str(move)+' Board[move]='+Board[move])		
		if move>-1 and Board[move]=='_':
			return move
		move= getMoveFromList([0,2,6,8])
		if move!=None:
			return move

		#check if center is available
		if Board[4]=='_':
			return 4
		#check if side-middles are available
		move =getMoveFromList([1, 3, 5, 7])
		if move!=None and Board[move]=='_':
			return move

#main loop
print('Welcome to Tic Tac Toe Game!')

while True:
	init_game();
	print(NextMover + ' starts with first move'+str(MoveCount))
	winner = None

	while MoveCount < 9:
		print_board()
		next_mover=NextMover
		if NextMover=='Player':
			symbol=PlayerSymbol
			move = getPlayerMoveLocation()
		else:
			symbol=CompSymbol
			move = getComputerMoveLocation()
		#returns True if this move make wins
		if makeMove(Board, symbol, move):
			winner=next_mover
			break
	print_board()
	print('')		
	if winner==None:
		print('## It was a draw.')
	else:
		print('## '+winner+ ' wins.')

	#if if user would like to play again
	print('Do you want to play again?[yes/no]:')
	playAgain = input().lower().startswith('y')
	if not playAgain:
		break
#############################END of the Tic Tac Toe Game##########


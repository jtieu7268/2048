from board import Board

def main():
    input('please press enter to play') # TODO: instructions
    bd = Board()
    print(bd)

    while not game_over(bd):
        dir = input().upper()
        while dir not in ["W","D","S","A"]:
            dir = input('enter valid move').upper() # TODO: clearer message
        bd.move(dir)
        print(bd)

def instructions():
    pass

def game_over(bd: Board):
    def got_2048():
        pass
    def no_legal_moves():
        pass
    pass

main()
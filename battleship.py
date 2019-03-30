class Board:
    user_board = []
    letters = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5,
                "G": 6, "H": 7, "I": 8, "J": 9}
    def create_board(self):
        size = 10
        for i in range(size):
            self.user_board.append([])
            for j in range(size):
                self.user_board[i].append('*')

    def print_board(self):
        size = 10
        print("Ваша доска:\n")
        for j in range(ord('A'), size + ord('A')):
            if (j == ord('A')):
                print("   ",end = " ")
            else:
                if (j != size + ord('A')-1):
                    print(chr(j-1), end = " ")
                else:
                    print(chr(j-1) + " " + chr(j))
        for i in range(size):
            if (i + 1 != size):
                print(i+1, " ",*self.user_board[i])
            else:
                print(i+1, "",*self.user_board[i])
        print("\n\n")

    def draw_ships(self):
        more = True
        print("Куда хотите поместить кораблик?\n\ Формат (А1, B7  и т.д.):")
        while (more):
            start = input("Начало корабля: ")
            s = self.letters.get(start[0], "none") #start letter
            se = int(start[1]) #start index
            end = input("Конец корабля: ")
            e = self.letters.get(end[0], "none") # end letter
            ee = int(end[1])
            if (ee == se):
                for i in range(s, e+1):
                    self.user_board[se-1][i] = "s"
            self.print_board()
            decision = input("Еще кораблик? (y/n)")
            more = True if (decision == "y") else False



    



print ("Добро пожаловать в игру Морской бой!\n\n")
my_board = Board()
my_board.create_board()
my_board.print_board()
my_board.draw_ships()



# start_game function
    # выбор вариант игры
    # стандартный режим 10 X 10
    # кастомный режим
        # 3 x 3
        # 7 X 7

# make_move function
import socket
import sys
user_board = []
size = 0

def define_size(game_mode):
    global size
    if game_mode == 1:
        size = 10
    elif game_mode == 2:
        size = 3
    else:
        size = 7
    

def create_board():
    global user_board
    for i in range(size):
        user_board.append([])
        for j in range(size):
            user_board[i].append('*')

# Correct way to ptint function
def print_board():
    print("Ваша доска:\n")
    for j in range(ord('A'), size + ord('A')):
        if (j == ord('A')):
            print(" ",end = " ")
        else:
            if (j != size + ord('A')-1):
                print(chr(j-1), end = " ")
            else:
                print(chr(j-1) + " " + chr(j))
    for i in range(size):
        print(i+1,*user_board[i])
    print("\n\n")


# Version with numbers
def print_board_version2():
    print("Ваша доска:\n")
    for i in range(size):
        if (i == 0):
            print(" ", end= " ")
        else:
            if (i != size - 1):
                print(i, end = " ")
            else:
                print(i, i+1)
    for j in range(size):
        print(j+1,*user_board[i])


print ("Добро пожаловать в игру Морской бой!\n\n")
print("В этой игре есть 3 режима:\n\n1.Стандратный режим 10 на 10\n2.Режим 3 на 3\n3.Режим 7 на 7\n")

flag = False
while(not flag):
    try:
        mode = int(input("Выберете режим(1,2 или 3): ")) # небезопасный каст
        if (mode >= 1 and mode <=3):
            flag = True
            define_size(mode)
            create_board()
        else:
            print("Введите число от 1 до 3!")
    except:
        print("Введите число от 1 до 3!")
        
print("* - пустая клетка\n0 - промах\n1 - попадание\ns - корабль\nx - ранение\n")

print_board()
print("\n")
print_board_version2()

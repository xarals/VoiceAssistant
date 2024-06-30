import tkinter as tk
from PIL import Image, ImageTk
import chess
from stockfish import Stockfish
from threading import Thread

class ChessBoard:
    def __init__(self, master, player_color):
        self.master = master
        self.master.title("Шахматная доска")
        self.player_color = player_color
        self.board2 = chess.Board()
        self.legal_moves = self.board2.legal_moves
        self.click_figure = -1
        self.board = tk.Canvas(self.master, width=600, height=600)
        self.board.pack()
        self.imgs = []
        self.imgs2 = []
        self.coords = []
        self.circles = []
        self.moves = []
        self.draw_board()
        self.place_pieces()
        self.coord_change = -1
        self.castl_white = True
        self.castl_black = True
        self.stockfish = Stockfish(path="stockfish\\stockfish_20011801_x64.exe")
        if self.player_color == 1:
            self.stockfish_move()
        #self.stockfish.set_elo_rating(elo)

    def stockfish_move(self):
        self.stockfish.set_fen_position(self.board2.fen())
        move = self.stockfish.get_best_move()
        self.move(move[:2], move[2:], False)


    def delete_circles(self):
        for img in self.circles:
            self.board.delete(img)
        self.circles = []

    def to_chess_coordinates(self, x, y):
        x1, y1 = -1, -1
        if self.player_color == 0:
            x1 = x // 75
            y1 = 8 - y // 75
        elif self.player_color == 1:
            x1 = 7 - x // 75
            y1 = y // 75 + 1
        w = ["a", "b", "c", "d", "e", "f", "g", "h"]
        x1 = w[x1]
        return f"{x1}{y1}"

    def to_coordinates(self, x_y):
        y = 8 - int(x_y[1])
        w = ["a", "b", "c", "d", "e", "f", "g", "h"]
        x = w.index(x_y[0])
        if self.player_color == 1:
            y = 7 - y
            x = 7 - w.index(x_y[0])
        return [x * 75, y * 75]

    def click_to(self, event):
        self.delete_circles()
        x_y = self.to_chess_coordinates(event.x, event.y)
        index = self.coords.index(x_y)
        self.click_figure = x_y
        self.moves = []
        for move in self.legal_moves:
            if str(move).startswith(x_y):
                to = str(move)[2] + str(move)[3]
                self.moves.append(to)
                coor = self.to_coordinates(to)
                self.place_piece(coor[0], coor[1], "images\\circle.png", True)

    def move(self, start, end, player):
        if start + end == "e1c1" and self.castl_white:
            c = self.to_coordinates("d1")
            self.board.coords(self.imgs[self.coords.index("a1")], c[0], c[1])
            self.coords[self.coords.index("a1")] = "d1"
        elif start + end == "e1g1" and self.castl_white:
            c = self.to_coordinates("f1")
            self.board.coords(self.imgs[self.coords.index("h1")], c[0], c[1])
            self.coords[self.coords.index("h1")] = "f1"
        elif start + end == "e8c8" and self.castl_black:
            c = self.to_coordinates("d8")
            self.board.coords(self.imgs[self.coords.index("a8")], c[0], c[1])
            self.coords[self.coords.index("a8")] = "d8"
        elif start + end == "e8g8" and self.castl_black:
            c = self.to_coordinates("f8")
            self.board.coords(self.imgs[self.coords.index("h8")], c[0], c[1])
            self.coords[self.coords.index("h8")] = "f8"
        if start == "e1":
            self.castl_white = False
        elif start == "e8":
            self.castl_black = False
        if player == False and len(end) > 2:
            if end in self.coords:
                rem = self.coords.index(end)
                self.coords.pop(rem)
                self.imgs.pop(rem)
            rem = self.coords.index(start)
            self.coords.pop(rem)
            self.imgs.pop(rem)
            if end[2] == "q":
                x_pos, y_pos = self.to_coordinates(end[0] + end[1])[0], self.to_coordinates(end[0] + end[1])[1]
                if self.player_color == 1:
                    piece = "images\\white_queen.png"
                else:
                    piece = "images\\black_queen.png"
                img = Image.open(piece).convert('RGBA')
                alpha = Image.new('RGBA', img.size, (0, 0, 0, 0))
                alpha.paste(img, (0, 0), img)
                img = ImageTk.PhotoImage(master=self.board, image=alpha)
                self.imgs.append(img)
                self.coords.append(self.to_chess_coordinates(x_pos, y_pos))
                self.board.create_image(x_pos, y_pos, image=img, anchor="nw", tags=(f"{img}",))
                self.board.tag_bind(f"{img}", "<Button-1>", self.click_to)
                self.board2.push_san(f"{start}{end}")
            elif end[2] == "n":
                x_pos, y_pos = self.to_coordinates(end[0] + end[1])[0], self.to_coordinates(end[0] + end[1])[1]
                if self.player_color == 1:
                    piece = "images\\white_knight.png"
                else:
                    piece = "images\\black_knight.png"
                img = Image.open(piece).convert('RGBA')
                alpha = Image.new('RGBA', img.size, (0, 0, 0, 0))
                alpha.paste(img, (0, 0), img)
                img = ImageTk.PhotoImage(master=self.board, image=alpha)
                self.imgs.append(img)
                self.coords.append(self.to_chess_coordinates(x_pos, y_pos))
                self.board.create_image(x_pos, y_pos, image=img, anchor="nw", tags=(f"{img}",))
                self.board.tag_bind(f"{img}", "<Button-1>", self.click_to)
                self.board2.push_san(f"{start}{end}")
            elif end[2] == "r":
                x_pos, y_pos = self.to_coordinates(end[0] + end[1])[0], self.to_coordinates(end[0] + end[1])[1]
                if self.player_color == 1:
                    piece = "images\\white_rook.png"
                else:
                    piece = "images\\black_rook.png"
                img = Image.open(piece).convert('RGBA')
                alpha = Image.new('RGBA', img.size, (0, 0, 0, 0))
                alpha.paste(img, (0, 0), img)
                img = ImageTk.PhotoImage(master=self.board, image=alpha)
                self.imgs.append(img)
                self.coords.append(self.to_chess_coordinates(x_pos, y_pos))
                self.board.create_image(x_pos, y_pos, image=img, anchor="nw", tags=(f"{img}",))
                self.board.tag_bind(f"{img}", "<Button-1>", self.click_to)
                self.board2.push_san(f"{start}{end}")
            elif end[2] == "b":
                x_pos, y_pos = self.to_coordinates(end[0] + end[1])[0], self.to_coordinates(end[0] + end[1])[1]
                if self.player_color == 1:
                    piece = "images\\white_bishop.png"
                else:
                    piece = "images\\black_bishop.png"
                img = Image.open(piece).convert('RGBA')
                alpha = Image.new('RGBA', img.size, (0, 0, 0, 0))
                alpha.paste(img, (0, 0), img)
                img = ImageTk.PhotoImage(master=self.board, image=alpha)
                self.imgs.append(img)
                self.coords.append(self.to_chess_coordinates(x_pos, y_pos))
                self.board.create_image(x_pos, y_pos, image=img, anchor="nw", tags=(f"{img}",))
                self.board.tag_bind(f"{img}", "<Button-1>", self.click_to)
                self.board2.push_san(f"{start}{end}")
            return
        to = self.to_coordinates(end)
        if end in self.coords:
            rem = self.coords.index(end)
            self.coords.pop(rem)
            self.imgs.pop(rem)
        self.board.coords(self.imgs[self.coords.index(start)], to[0], to[1])
        self.coords[self.coords.index(start)] = end
        try:
            self.board2.push_san(start + end)
        except:
            pass
        if player:
            th = Thread(target=self.stockfish_move)
            th.start()

    def new_white_queen(self, event):
        x_pos, y_pos = self.to_coordinates(self.coord_change)[0], self.to_coordinates(self.coord_change)[1]
        img = Image.open("images\\white_queen.png").convert('RGBA')
        alpha = Image.new('RGBA', img.size, (0, 0, 0, 0))
        alpha.paste(img, (0, 0), img)
        img = ImageTk.PhotoImage(master=self.board, image=alpha)
        self.imgs.append(img)
        self.coords.append(self.to_chess_coordinates(x_pos, y_pos))
        self.board.create_image(x_pos, y_pos, image=img, anchor="nw", tags=(f"{img}",))
        self.board.tag_bind(f"{img}", "<Button-1>", self.click_to)
        x_y = self.coord_change
        index = self.coords.index(x_y)
        self.coords.pop(index)
        self.imgs.pop(index)
        self.board2.push_san(f"{self.click_figure}{self.coord_change}q")
        for img in self.imgs2:
            self.board.delete(img)
        self.imgs2 = []

    def new_white_rook(self, event):
        x_pos, y_pos = self.to_coordinates(self.coord_change)[0], self.to_coordinates(self.coord_change)[1]
        img = Image.open("images\\white_rook.png").convert('RGBA')
        alpha = Image.new('RGBA', img.size, (0, 0, 0, 0))
        alpha.paste(img, (0, 0), img)
        img = ImageTk.PhotoImage(master=self.board, image=alpha)
        self.imgs.append(img)
        self.coords.append(self.to_chess_coordinates(x_pos, y_pos))
        self.board.create_image(x_pos, y_pos, image=img, anchor="nw", tags=(f"{img}",))
        self.board.tag_bind(f"{img}", "<Button-1>", self.click_to)
        x_y = self.coord_change
        index = self.coords.index(x_y)
        self.coords.pop(index)
        self.imgs.pop(index)
        self.board2.push_san(f"{self.click_figure}{self.coord_change}r")
        for img in self.imgs2:
            self.board.delete(img)
        self.imgs2 = []

    def new_white_knight(self, event):
        x_pos, y_pos = self.to_coordinates(self.coord_change)[0], self.to_coordinates(self.coord_change)[1]
        img = Image.open("images\\white_knight.png").convert('RGBA')
        alpha = Image.new('RGBA', img.size, (0, 0, 0, 0))
        alpha.paste(img, (0, 0), img)
        img = ImageTk.PhotoImage(master=self.board, image=alpha)
        self.imgs.append(img)
        self.coords.append(self.to_chess_coordinates(x_pos, y_pos))
        self.board.create_image(x_pos, y_pos, image=img, anchor="nw", tags=(f"{img}",))
        self.board.tag_bind(f"{img}", "<Button-1>", self.click_to)
        x_y = self.coord_change
        index = self.coords.index(x_y)
        self.coords.pop(index)
        self.imgs.pop(index)
        self.board2.push_san(f"{self.click_figure}{self.coord_change}n")
        for img in self.imgs2:
            self.board.delete(img)
        self.imgs2 = []

    def new_white_bishop(self, event):
        x_pos, y_pos = self.to_coordinates(self.coord_change)[0], self.to_coordinates(self.coord_change)[1]
        img = Image.open("images\\white_bishop.png").convert('RGBA')
        alpha = Image.new('RGBA', img.size, (0, 0, 0, 0))
        alpha.paste(img, (0, 0), img)
        img = ImageTk.PhotoImage(master=self.board, image=alpha)
        self.imgs.append(img)
        self.coords.append(self.to_chess_coordinates(x_pos, y_pos))
        self.board.create_image(x_pos, y_pos, image=img, anchor="nw", tags=(f"{img}",))
        self.board.tag_bind(f"{img}", "<Button-1>", self.click_to)
        x_y = self.coord_change
        index = self.coords.index(x_y)
        self.coords.pop(index)
        self.imgs.pop(index)
        self.board2.push_san(f"{self.click_figure}{self.coord_change}b")
        for img in self.imgs2:
            self.board.delete(img)
        self.imgs2 = []

    def new_black_queen(self, event):
        x_pos, y_pos = self.to_coordinates(self.coord_change)[0], self.to_coordinates(self.coord_change)[1]
        img = Image.open("images\\black_queen.png").convert('RGBA')
        alpha = Image.new('RGBA', img.size, (0, 0, 0, 0))
        alpha.paste(img, (0, 0), img)
        img = ImageTk.PhotoImage(master=self.board, image=alpha)
        self.imgs.append(img)
        self.coords.append(self.to_chess_coordinates(x_pos, y_pos))
        self.board.create_image(x_pos, y_pos, image=img, anchor="nw", tags=(f"{img}",))
        self.board.tag_bind(f"{img}", "<Button-1>", self.click_to)
        x_y = self.coord_change
        index = self.coords.index(x_y)
        self.coords.pop(index)
        self.imgs.pop(index)
        self.board2.push_san(f"{self.click_figure}{self.coord_change}q")
        for img in self.imgs2:
            self.board.delete(img)
        self.imgs2 = []

    def new_black_rook(self, event):
        x_pos, y_pos = self.to_coordinates(self.coord_change)[0], self.to_coordinates(self.coord_change)[1]
        img = Image.open("images\\black_rook.png").convert('RGBA')
        alpha = Image.new('RGBA', img.size, (0, 0, 0, 0))
        alpha.paste(img, (0, 0), img)
        img = ImageTk.PhotoImage(master=self.board, image=alpha)
        self.imgs.append(img)
        self.coords.append(self.to_chess_coordinates(x_pos, y_pos))
        self.board.create_image(x_pos, y_pos, image=img, anchor="nw", tags=(f"{img}",))
        self.board.tag_bind(f"{img}", "<Button-1>", self.click_to)
        x_y = self.coord_change
        index = self.coords.index(x_y)
        self.coords.pop(index)
        self.imgs.pop(index)
        self.board2.push_san(f"{self.click_figure}{self.coord_change}r")
        for img in self.imgs2:
            self.board.delete(img)
        self.imgs2 = []

    def new_black_knight(self, event):
        x_pos, y_pos = self.to_coordinates(self.coord_change)[0], self.to_coordinates(self.coord_change)[1]
        img = Image.open("images\\black_knight.png").convert('RGBA')
        alpha = Image.new('RGBA', img.size, (0, 0, 0, 0))
        alpha.paste(img, (0, 0), img)
        img = ImageTk.PhotoImage(master=self.board, image=alpha)
        self.imgs.append(img)
        self.coords.append(self.to_chess_coordinates(x_pos, y_pos))
        self.board.create_image(x_pos, y_pos, image=img, anchor="nw", tags=(f"{img}",))
        self.board.tag_bind(f"{img}", "<Button-1>", self.click_to)
        x_y = self.coord_change
        index = self.coords.index(x_y)
        self.coords.pop(index)
        self.imgs.pop(index)
        self.board2.push_san(f"{self.click_figure}{self.coord_change}n")
        for img in self.imgs2:
            self.board.delete(img)
        self.imgs2 = []

    def new_black_bishop(self, event):
        x_pos, y_pos = self.to_coordinates(self.coord_change)[0], self.to_coordinates(self.coord_change)[1]
        img = Image.open("images\\black_bishop.png").convert('RGBA')
        alpha = Image.new('RGBA', img.size, (0, 0, 0, 0))
        alpha.paste(img, (0, 0), img)
        img = ImageTk.PhotoImage(master=self.board, image=alpha)
        self.imgs.append(img)
        self.coords.append(self.to_chess_coordinates(x_pos, y_pos))
        self.board.create_image(x_pos, y_pos, image=img, anchor="nw", tags=(f"{img}",))
        self.board.tag_bind(f"{img}", "<Button-1>", self.click_to)
        x_y = self.coord_change
        index = self.coords.index(x_y)
        self.coords.pop(index)
        self.imgs.pop(index)
        self.board2.push_san(f"{self.click_figure}{self.coord_change}b")
        for img in self.imgs2:
            self.board.delete(img)
        self.imgs2 = []

    def change_figure(self, coord):
        print("Start")
        self.coord_change = coord
        if self.player_color == 0:
            pieces = ["images\\white_rook.png", "images\\white_knight.png", "images\\white_bishop.png", "images\\white_queen.png"]
        else:
            pieces = ["images\\black_rook.png", "images\\black_knight.png", "images\\black_bishop.png", "images\\black_queen.png"]
        k = 0
        for piece in pieces:
            img = Image.open(piece).convert('RGBA')
            alpha = Image.new('RGBA', img.size, (0, 0, 0, 0))
            alpha.paste(img, (0, 0), img)
            img = ImageTk.PhotoImage(master=self.board, image=alpha)
            self.imgs2.append(img)
            self.board.create_image(150 + k, 287, image=img, anchor="nw", tags=(f"{img}",))
            if piece == "images\\white_queen.png":
                self.board.tag_bind(f"{img}", "<Button-1>", self.new_white_queen)
            elif piece == "images\\white_rook.png":
                self.board.tag_bind(f"{img}", "<Button-1>", self.new_white_rook)
            elif piece == "images\\white_knight.png":
                self.board.tag_bind(f"{img}", "<Button-1>", self.new_white_knight)
            elif piece == "images\\white_bishop.png":
                self.board.tag_bind(f"{img}", "<Button-1>", self.new_white_bishop)
            elif piece == "images\\black_queen.png":
                self.board.tag_bind(f"{img}", "<Button-1>", self.new_black_queen)
            elif piece == "images\\black_rook.png":
                self.board.tag_bind(f"{img}", "<Button-1>", self.new_black_rook)
            elif piece == "images\\black_knight.png":
                self.board.tag_bind(f"{img}", "<Button-1>", self.new_black_knight)
            elif piece == "images\\black_bishop.png":
                self.board.tag_bind(f"{img}", "<Button-1>", self.new_black_bishop)
            k += 75

    def click_circle(self, event):
        self.delete_circles()
        x_y = self.to_chess_coordinates(event.x, event.y)
        for move in self.legal_moves:
            if str(move).startswith(self.click_figure + x_y) and len(str(move)) > 4:
                self.change_figure(x_y)
                break
        self.move(self.click_figure, x_y, True)

    def draw_board(self):
        colors = ["#f1d0a7", "#c26933"]
        for i in range(8):
            for j in range(8):
                x1 = i * 75
                y1 = j * 75
                x2 = x1 + 100
                y2 = y1 + 100
                color = colors[(i+j)%2]
                self.board.create_rectangle(x1, y1, x2, y2, fill=color)

    def place_pieces(self):
        pieces = {
            "wr": "images\\white_rook.png",
            "wn": "images\\white_knight.png",
            "wb": "images\\white_bishop.png",
            "wq": "images\\white_queen.png",
            "wk": "images\\white_king.png",
            "wp": "images\\white_pawn.png",
            "br": "images\\black_rook.png",
            "bn": "images\\black_knight.png",
            "bb": "images\\black_bishop.png",
            "bq": "images\\black_queen.png",
            "bk": "images\\black_king.png",
            "bp": "images\\black_pawn.png"
        }
        y = 0
        if self.player_color == 1:
            y = 7
        for i in range(8):
            self.place_piece(i, abs(y - 1), pieces["bp"], False)
            self.place_piece(i, abs(y - 6), pieces["wp"], False)
        for i in [0, 7]:
            self.place_piece(i, abs(y - 0), pieces["br"], False)
            self.place_piece(i, abs(y - 7), pieces["wr"], False)
        for i in [1, 6]:
            self.place_piece(i, abs(y - 0), pieces["bn"], False)
            self.place_piece(i, abs(y - 7), pieces["wn"], False)
        for i in [2, 5]:
            self.place_piece(i, abs(y - 0), pieces["bb"], False)
            self.place_piece(i, abs(y - 7), pieces["wb"], False)
        x = 7
        if self.player_color == 0:
            x = 0
        self.place_piece(abs(x - 3), abs(y - 0), pieces["bq"], False)
        self.place_piece(abs(x - 3), abs(y - 7), pieces["wq"], False)
        self.place_piece(abs(x - 4), abs(y - 0), pieces["bk"], False)
        self.place_piece(abs(x - 4), abs(y - 7), pieces["wk"], False)

    def place_piece(self, x, y, piece, circle):
        x_pos = x * 75
        y_pos = y * 75
        if circle:
            x_pos = x
            y_pos = y
        img = Image.open(piece).convert('RGBA')
        alpha = Image.new('RGBA', img.size, (0, 0, 0, 0))
        alpha.paste(img, (0, 0), img)
        img = ImageTk.PhotoImage(master=self.board, image=alpha)
        if circle:
            self.circles.append(img)
        else:
            self.imgs.append(img)
            self.coords.append(self.to_chess_coordinates(x_pos, y_pos))
        self.board.create_image(x_pos, y_pos, image=img, anchor="nw", tags=(f"{img}",))
        if circle:
            self.board.tag_bind(f"{img}", "<Button-1>", self.click_circle)
        elif (piece.startswith("images\\white") and self.player_color == 0) or (piece.startswith("images\\black") and self.player_color == 1):
            self.board.tag_bind(f"{img}", "<Button-1>", self.click_to)

    def get_piece(self, i):
        pieces = ["r", "n", "b", "q", "k", "b", "n", "r"]
        return pieces[i]

def play(color):
    root = tk.Tk()
    board = ChessBoard(root, color)
    root.mainloop()
import ChessEngine, ChessAI
import pygame as p



WIDTH = 700
HEIGHT = 512
quantity = 8
SquareSize = HEIGHT // quantity
maxfps = 30
images = {}
reset_img = p.image.load("imgs/reset.png")
team_img = p.image.load("imgs/team.png")
gr_img = p.image.load("imgs/group.png")
close_img = p.image.load("imgs/close.png")
restar_img = p.image.load("imgs/restart.png")
lose_img = p.image.load("imgs/lose.png")
win_img = p.image.load("imgs/winner.png")
draw_img = p.image.load("imgs/draw.png")



def loadImages():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        images[piece] = p.image.load("imgs/" + piece + ".png")


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    p.draw.rect(screen, "black", (512, 0, 188, 100))
    screen.blit(gr_img, p.Rect(512, 0, 188, 100))
    p.draw.rect(screen, "black", (512, 100, 188, 200))
    screen.blit(team_img, p.Rect(512, 100, 188, 200))
    p.draw.rect(screen, "white", (534, 350, 60, 60))
    screen.blit(reset_img, p.Rect(534, 350, 60, 60))
    p.draw.rect(screen, "white", (616, 350, 60, 60))
    screen.blit(close_img, p.Rect(616, 350, 60, 60))
    p.draw.rect(screen, "white", (556, 430, 100, 60))
    screen.blit(restar_img, p.Rect(556, 430, 100, 60))

    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages()
    running = True
    gameOver = False

    sqSelected = ()
    playerClicks = []



    playerOne = False
    playerTwo = False

    while running:

        human_turn = (gs.white_to_move and playerOne) or (not gs.white_to_move and playerTwo)

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and human_turn:
                    location = p.mouse.get_pos()
                    if location[0] <= HEIGHT and location[1] <= HEIGHT:
                        col = location[0] // SquareSize
                        row = location[1] // SquareSize
                        if sqSelected == (row, col):
                            sqSelected = ()
                            playerClicks = []
                        else:
                            sqSelected = (row, col)
                            playerClicks.append(sqSelected)

                        if len(playerClicks) == 2 and human_turn:
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                            print(move.getChessNotation())
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    gs.makeMove(validMoves[i])
                                    moveMade = True
                                    sqSelected = ()
                                    playerClicks = []
                            if not moveMade:
                                playerClicks = [sqSelected]

                    elif 616 <= location[0] <= 666 and 350 <= location[1] <= 410:
                        running = False


                    elif 534 <= location[0] <= 594 and 350 <= location[1] <= 410: #undo
                        gs.undoMove()
                        sqSelected = ()
                        playerClicks = []
                        moveMade = True



                    elif 556 <= location[0] <= 616 and 430 <= location[1] <= 490: # reset
                        gs = ChessEngine.GameState()
                        validMoves = gs.getValidMoves()
                        sqSelected = ()
                        playerClicks = []
                        moveMade  = False
                        gameOver = False



        drawGameState(screen, gs, validMoves, sqSelected)

        #AI
        if not gameOver and not human_turn:
            print("\n-----Thinking-----\n")
            ai_move = ChessAI.findBestMove(gs, validMoves)
            if ai_move is None:
                ai_move = ChessAI.findRandomMove(validMoves)
            print("\n-----Done-----\n")
            gs.makeMove(ai_move)
            moveMade = True


        if moveMade:
            print(gs.white_to_move, "is white")
            validMoves = gs.getValidMoves()
            moveMade = False



        if gs.checkmate:
            gameOver = True
            if e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                if 556 <= location[0] <= 616 and 430 <= location[1] <= 490:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    gameOver = False



            if gs.white_to_move:
                screen.blit(lose_img, p.Rect(192, 192, 128, 128))

            else:
                screen.blit(win_img, p.Rect(192, 192, 128, 128))

        if gs.stalemate:
            gameOver = True
            screen.blit(draw_img, p.Rect(192, 192, 128, 128))
            if e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                if 556 <= location[0] <= 616 and 430 <= location[1] <= 490:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    gameOver = False


        clock.tick(maxfps)
        p.display.flip()

def hightLight(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        row, col = sqSelected
        if gs.board[row][col][0] == (
                'w' if gs.white_to_move else 'b'):
            s = p.Surface((SquareSize, SquareSize))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (col * SquareSize, row * SquareSize))
            s.fill(p.Color('green'))
            for move in validMoves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(s, (move.end_col * SquareSize, move.end_row * SquareSize))




def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    drawPieces(screen, gs.board)
    hightLight(screen, gs, validMoves, sqSelected)


def drawBoard(screen):
    colours = [p.Color("white"), p.Color("#93d3ff")]
    for r in range(quantity):
        for c in range(quantity):
            colour = colours[((r + c) % 2)]
            p.draw.rect(screen, colour, p.Rect(c * SquareSize, r * SquareSize, SquareSize, SquareSize))


def drawPieces(screen, board):
    for r in range(quantity):
        for c in range(quantity):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], p.Rect(c * SquareSize, r * SquareSize, SquareSize, SquareSize))



if __name__ == "__main__":
    main()
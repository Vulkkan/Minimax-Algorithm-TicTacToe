class Minimax:
    def __init__(self, bot, player):
        self.bot = bot
        self.opponent = player

    def isMovesLeft(self, board):
        for row in board:
            if '_' in row:
                return True
        return False

    def evaluate(self, b):
        for row in range(3):
            if b[row][0] == b[row][1] == b[row][2] != '_':
                return 10 if b[row][0] == self.bot else -10

        for col in range(3):
            if b[0][col] == b[1][col] == b[2][col] != '_':
                return 10 if b[0][col] == self.bot else -10

        if b[0][0] == b[1][1] == b[2][2] != '_':
            return 10 if b[0][0] == self.bot else -10

        if b[0][2] == b[1][1] == b[2][0] != '_':
            return 10 if b[0][2] == self.bot else -10

        return 0

    def minimax(self, board, depth, isMax):
        score = self.evaluate(board)
        if score in [10, -10]:
            return score
        if not self.isMovesLeft(board):
            return 0

        if isMax:
            best = -1000
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '_':
                        board[i][j] = self.bot
                        best = max(best, self.minimax(board, depth + 1, not isMax))
                        board[i][j] = '_'
            return best
        else:
            best = 1000
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '_':
                        board[i][j] = self.opponent
                        best = min(best, self.minimax(board, depth + 1, not isMax))
                        board[i][j] = '_'
            return best

    def findBestMove(self, board):
        bestVal = -1000
        bestMove = (-1, -1)

        for i in range(3):
            for j in range(3):

                if board[i][j] == '_':

                    board[i][j] = self.bot
                    moveVal = self.minimax(board, 1, False)
                    board[i][j] = '_'
                    if moveVal > bestVal:
                        bestMove = (i, j)
                        bestVal = moveVal
                        
        return bestMove
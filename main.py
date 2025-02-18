from kivymd.uix.backdrop.backdrop import MDTopAppBar
from kivymd.uix.snackbar import MDSnackbar
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog

from kivy.animation import Animation
from kivy.clock import Clock
from random import sample, choice
from bot_algorithm import Minimax
import os, sys
from kivy.resources import resource_add_path, resource_find

import utils, game_functions


class PvBotSetupScreen(Screen):
    pass
class PvBotPositionSelectionScreen(Screen):
    pass
class GameScreen(Screen):
    pass


class TicTacToeButton(MDRaisedButton):
    def __init__(self, index, **kwargs):
        super().__init__(**kwargs)
        self.index = index
        

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'BlueGray'
        self.root = Builder.load_file('ui/ui.kv')

        self.winner = False
        self.is_finish = False
        self.player_name = ''
        self.bot_move_scheduled = False

        self.game_screen = self.root.get_screen('game_screen')
        utils.init_screens(self)
        
        return self.root


    '''Functions for making a move'''
    def player_execute(self, button):
        self.game_screen.ids.player_thinking.text = ''

        if not self.is_finish:
            button.text = self.player_choice
            button.disabled = True
            utils.p[button.index] = self.player_choice
            self.lead_round(self.bot_choice)


    def bot_execution(self):
        if not self.bot_move_scheduled:
            game_screen = self.root.get_screen("game_screen")

            game_screen.ids.bot_thinking.text = utils.bot_thinking_text
            game_screen.ids.player_thinking.text = ''

            self.bot_move_scheduled = True
            Clock.schedule_once(lambda dt: self.bot_move(), 0.8)


    def bot_move(self):
        game_screen = self.root.get_screen("game_screen")

        # Convert self.p (1D board) to 2D format expected by Minimax
        game_board = [[utils.p[i] if isinstance(utils.p[i], str) else '_' for i in range(3)],
                    [utils.p[i+3] if isinstance(utils.p[i+3], str) else '_' for i in range(3)],
                    [utils.p[i+6] if isinstance(utils.p[i+6], str) else '_' for i in range(3)]]
        
        # Get the best move (row, col) using Minimax
        best_move = self.minimax.findBestMove(game_board)

        if best_move:
            row, col = best_move  # Unpack best move
            button_index = row * 3 + col  # Convert 2D coordinates to 1D index (0 to 8)

            # Access the corresponding button by index
            button = game_screen.ids.grid.children[8 - button_index]  # Grid's children are in reverse order
            button.text = self.bot_choice
            button.disabled = True
            
            # Update the internal board state to reflect the bot's move
            utils.p[button_index] = self.bot_choice
            
            # Hand over control to the player after bot's move
            self.lead_round(self.player_choice)
            
        # Clear the scheduled flag
        game_screen.ids.player_thinking.text = utils.player_thinking_text
        game_screen.ids.bot_thinking.text = ''
        self.bot_move_scheduled = False


    def lead_round(self, whose_turn):
        game_functions.check_winner(self)

        if self.is_finish:
            return
        
        # Check if all moves are filled (tie condition)
        if all(isinstance(x, str) for x in utils.p):  
            game_functions.finalization(self, False)
            return

        # Continue the game if there's no winner or tie
        if whose_turn == self.bot_choice and not self.is_finish:
            self.bot_execution()


    def start_game(self, player_choice):
        self.player_choice = player_choice
        self.bot_choice = 'O' if player_choice == 'X' else 'X'

        self.minimax = Minimax(self.bot_choice, self.player_choice)
        
        game_screen = self.root.get_screen("game_screen")
        game_screen.ids.players_label.text = f"{self.player_name} as {self.player_choice} \nvs\n Bot as {self.bot_choice}"

        # Set up the grid buttons
        for i in range(9):
            btn = TicTacToeButton(index=i, text="", on_release=self.player_execute)
            btn.size_hint = (1, 1)
            btn.md_bg_color = utils.board_colors['bluegray']
            game_screen.ids.grid.add_widget(btn)

        if self.player_choice == 'X':
            game_screen.ids.player_thinking.text = utils.player_thinking_text

        # Player selects O, Bot goes first
        if self.bot_choice == 'X':
            game_screen.ids.bot_thinking.text = utils.bot_thinking_text
            Clock.schedule_once(lambda dt: self.bot_execution(), 0.8)

    def show_result_popup(self, message):
        self.result_diag = MDDialog(
            title="Game Over",
            text=message,
            buttons=[
                MDFlatButton(
                    text="Play Again",
                    on_release=self.reset_game,
                ),
                MDFlatButton(
                    text="Quit",
                    md_bg_color = utils.board_colors['orange'],
                    on_release=lambda x: game_functions.quit_game(self),
                ),
            ],
        )
        self.result_diag.open()


    def reset_game(self, *args):
        self.result_diag.dismiss()

        game_screen = self.root.get_screen("game_screen")
        game_screen.ids.grid.clear_widgets()
        
        utils.p = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.winner = False
        self.is_finish = False
        self.bot_move_scheduled = False
        
        # Reinitialize grid buttons with default settings
        for i in range(9):
            btn = TicTacToeButton(index=i, text="", on_release=self.player_execute)
            btn.size_hint = (1, 1)  # Ensure size_hint consistence
            btn.md_bg_color = utils.board_colors['bluegray']

            game_screen.ids.grid.add_widget(btn)
    
        # Start bot move if player chose O
        if self.bot_choice == 'X':
            self.bot_execution()

    def exit(self):
        game_functions.exit(self)

    


if __name__ == "__main__":
    if hasattr(sys,'_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    MainApp().run()
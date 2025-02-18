from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog

import utils


def check_winner(app):
    game_screen = app.root.get_screen("game_screen")

    for pos in utils.winning_positions:
        if utils.p[pos[0]] == utils.p[pos[1]] == utils.p[pos[2]]:
            app.is_finish = True
            app.winner = utils.p[pos[0]]
            animate_winning_boxes(app, pos)
            return

def animate_winning_boxes(app, winning_pos):
    game_screen = app.root.get_screen("game_screen")
    
    def animate_box(index, delay):
        button = game_screen.ids.grid.children[8 - index]
        anim = Animation(size_hint=(1.2, 1.2), duration=0.3) + Animation(size_hint=(1, 1), duration=0.3)
        anim.bind(on_complete=lambda *args: setattr(button, "md_bg_color", [1, 0.5, 0, 1]))  # Set to green
        anim.start(button)

    for i, pos in enumerate(winning_pos):
        Clock.schedule_once(lambda dt, idx=pos: animate_box(idx, i), i * 0.5)

    Clock.schedule_once(lambda dt: finalization(app, True), len(winning_pos) * 0.5 + 0.5)


def exit(app):
    def quit_game():
        game_screen = app.root.get_screen("game_screen")
        game_screen.ids.grid.clear_widgets()

        utils.p = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        app.winner = False
        app.is_finish = False
        app.bot_move_scheduled = False

        app.dialog.dismiss()
        app.root.current = 'pvbot_setup_screen'

    app.dialog = MDDialog(
        title="Quit",
        text=f"You really gonna chicken out??",
        buttons=[
            MDFlatButton(
                text="Keep playing",
                on_release=lambda x: app.dialog.dismiss()
            ),
            MDRaisedButton(
                text="Exit",
                md_bg_color = utils.board_colors['orange'],
                on_release=lambda *x: quit_game()
            )
        ]
    )
    app.dialog.open()



def quit_game(app):
    game_screen = app.root.get_screen("game_screen")
    game_screen.ids.grid.clear_widgets()

    utils.p = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    app.winner = False
    app.is_finish = False
    app.bot_move_scheduled = False

    # self.res_dialog.dismiss()
    app.root.current = 'pvbot_selection_screen'
    app.result_diag.dismiss()


def finalization(app, games_end):
    msg = utils.get_random_message(games_end, app.winner, app.bot_choice)
    app.show_result_popup(msg)
    app.is_finish = True
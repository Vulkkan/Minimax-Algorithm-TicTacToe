import random


winning_positions: list[list[int]] = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]
p: list[int]= [1, 2, 3, 4, 5, 6, 7, 8, 9]

board_colors : dict[str, list[int]]= {
    'red': [1, 0, 0, 1],
    'green': [0, 1, 0, 1],
    'blue': [0, 0, 1, 1],
    'bluegray': [0.376, 0.490, 0.545, 1],
    'orange': [1, 0.5, 0, 1],
    'purple': [0.3, 0, 0.6, 1],
    'pink': [1, 0.75, 0.8, 1],
    'brown': [0.6, 0.3, 0.1, 1],
    'lime': [0, 1, 0.5, 1],
    'teal': [0, 0.5, 0.5, 1],
    'navy': [0, 0, 0.5, 1],
    'olive': [0.5, 0.5, 0, 1],
    'salmon': [1, 0.5, 0.5, 1],
    'gold': [1, 0.84, 0, 1],
    'violet': [0.5, 0, 1, 1],
}

theme_colors =  [
    'Red','Pink', 'Purple', 'DeepPurple', 'Indigo', 
    # 'Blue', 'LightBlue', 'Cyan', 
    'Teal', 'Green', 'LightGreen', 'Lime', 
    'Yellow', 'Amber', 
    'Orange', 'DeepOrange', 'Brown', 
    'Gray', 'BlueGray'
]

# ids: list[str] = [
#     'playerOThinking',
#     'pvpLabel',
#     'playerXThinkingLabel',
# player_avatar, bot_avatar

#     'bot_thinking',
#     'players_label',
#     'player_thinking',

#     'name_input',
#     'playerX_txt',
#     'playerO_txt'
# ]

player_thinking_text: str = 'Your turn'
bot_thinking_text: str = 'Thinking..'

appTitleTxT = '[color=556677]Tic[/color][color=FF6400]Tac[/color][color=334456]Toe[/color]'

appTitle = '[color=556677]x[/color][color=FF6400]O[/color]\n[color=FF6400]o[/color][color=556677]X[/color]'



def get_random_message(games_end, winner, bot_choice) -> any:
    win_messages: list[str] = [
        "Oh wow. You won. Crazy!", 
        "Victory!",
        "Amazing! You beat the bot!",
    ]
    lose_messages: list[str] = [
        "Loser!", 
        "Fatality!", 
        "You got smashed!",
        "Defeated!",
    ]
    tie_message: str = "That was a tie. You're smart bro NGL"
    
    if not games_end:
        return tie_message
    elif winner == bot_choice:
        return random.choice(lose_messages)
    else:
        return random.choice(win_messages)


def init_screens(app):
    setup_screen = app.root.get_screen('pvbot_setup_screen')
    game_screen = app.root.get_screen('game_screen')
    selection_screen = app.root.get_screen('pvbot_selection_screen')

    setup_screen.ids.appTitle.text = appTitle
    selection_screen.ids.appTitle.text = appTitle

    game_screen.ids.appTitle.text = appTitleTxT
    game_screen.ids.playerAvatar.text_color = board_colors['bluegray']
    game_screen.ids.botAvatar.text_color = board_colors['bluegray']

    game_screen.ids.quitBtn.md_bg_color = [0.20, 0.26, 0.30, 1]
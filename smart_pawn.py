import pandas as pd
import numpy as np

class SmartPawn:
    aggressive = {}
    kind = {}
    Strategy = {}
    def __init__(self, player_mode):
        pawns = [F"P{i}_pawn{j}" for i in range(player_mode) for j in range(4)]
        pawns_mode = [mode for mode in player_mode for _ in range(4)]
        initial_loc = ["not_in_game" for _ in range(0, player_mode*4)]
        self.main_df = pd.DataFrame({
            "pawn_id": pawns,
            "mode": pawns_mode,
            "loc": initial_loc
        })

    def move(self, player, rolled_number):
        target_pawns_df = self.main_df[~self.main_df['pawn_id'].str.startswith(F"P{player}_")]
        loc_target_pawns = target_pawns_df["loc"].values
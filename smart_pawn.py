import pandas as pd
import numpy as np

class SmartPawn:
    count_homes = 47
    aggressive = {"can_move_rate": 0.01, "can_hit_rate": 0.8, "can_come_in_game_rate": 0.5, "can_end_round_rate": 0.5}
    kind = {"can_move_rate": 0.01, "can_hit_rate": 0.01, "can_come_in_game_rate": 0.7, "can_end_round_rate": 0.8}
    strategy = {"can_move_rate": 0.01, "can_hit_rate": 0.5, "can_come_in_game_rate": 0.6, "can_end_round_rate": 0.8}
    stupid = {"can_move_rate": 0.01, "can_hit_rate": 0.01, "can_come_in_game_rate": 0.8, "can_end_round_rate": 0.1}
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

        pawns_profile = pd.DataFrame(
            self.__make_pawns_profile(player, rolled_number, target_pawns_df, loc_target_pawns),
            index=[f"P{player}_pawn{i}" for i in range(4)]
        )        
        print(pawns_profile)
    
    # private methods:

    def __make_pawns_profile(self, player, rolled_number, target_pawns_df, loc_target_pawns):
        can_move = [self.__can_move(F"P{player}_pawn{i}") for i in range(4)]

        can_hit = [self.__can_hit(F"P{player}_pawn{i}", rolled_number, loc_target_pawns) for i in range(4)]

        if rolled_number == 6:
            can_come_in_game = [self.__can_come_in_game(F"P{player}_pawn{i}") for i in range(4)]
        else:
            can_come_in_game = [0 for _ in range(4)]
        
        can_end_round = [self.__can_end_round(F"P{player}_pawn{i}", rolled_number) for i in range(4)]

        return {"can_move": can_move,
                "can_hit": can_hit,
                "can_come_in_game": can_come_in_game,
                "can_end_round": can_end_round}
    
    def __can_move(self, pawn_id):
        pos_pawn = self.main_df.loc[self.main_df["pawn_id"] == pawn_id, "position"].values[0]
        if pos_pawn == "in game":
            return 1
        else:
            return 0

    def __can_hit(self, pawn_id, rolled_number, loc_target_pawns):
        loc_pawn = self.main_df.loc[self.main_df["pawn_id"] == pawn_id, "loc"].values[0]
        if loc_pawn in ["not in game", "finish game"]:
            return 0
        
        loc_pawn += rolled_number
        if loc_pawn > 47:
            loc_pawn = loc_pawn - 47
            # 47, Number of houses in the game
        
        if loc_pawn in loc_target_pawns:
            return 1
        else:
            return 0
        
    def __can_come_in_game(self, pawn_id):
        pos_pawn = self.main_df.loc[self.main_df["pawn_id"] == pawn_id, "position"].values[0]

        if pos_pawn == "not in game":
            return 1
        else:
            return 0
    
    def __can_end_round(self, pawn_id, rolled_number):
        player = pawn_id[:2]

        pos_pawn = self.main_df.loc[self.main_df['pawn_id'] == pawn_id, "position"].values[0]
        if pos_pawn == "not in game":
            return 0
        
        loc_pawn = self.main_df.loc[self.main_df['pawn_id'] == pawn_id, "loc"].values[0]
        for i in range(1, rolled_number+1):
            loc_pawn += 1
            if loc_pawn == self.home_zone[player]:
                num_home_zone_pawn = (rolled_number - i) + 1
                if num_home_zone_pawn in [1, 2, 3, 4]: 
                    full_home_zone = self.main_df[self.main_df["pawn_id"].str.startswith(player)]["num_home_zone"].values
                    if not num_home_zone_pawn in full_home_zone:
                        return 1
                    else: 
                        return 0
                else:
                    return 0
            else:
                return 0
        return 0
    
    def __distance_home_zone(self, pawn_id):
        pos_pawn = self.main_df.loc[self.main_df["pawn_id"] == pawn_id, "position"].values[0]
        if pos_pawn != "in game":
            return -1

        player = pawn_id[:2]
        loc_pawn = self.main_df.loc[self.main_df["pawn_id"] == pawn_id, "loc"].values[0]

        if loc_pawn in range(self.start_zone[player], self.count_homes + 1):
            distance = (self.count_homes - loc_pawn) + self.home_zone[player]
        else:
            distance = self.home_zone[player] - loc_pawn
        return distance


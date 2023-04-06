# -*- coding: utf-8 -*-
''' Implement Swy-blm Game class
'''
import functools
from heapq import merge
import numpy as np

from rlcard.games.swy_blm.utils import SwyBlmDealer
from rlcard.games.swy_blm.utils import _cards2array, _cards2table


class SwyBlmGame:
    ''' Provide game APIs for env to run swy-blm and get corresponding state
    information.
    '''
    def __init__(self, allow_step_back=False):
        self.allow_step_back = allow_step_back
        self.np_random = np.random.RandomState()
        self.num_players = 2
        self.num_actions = 44

    def init_game(self):
        ''' Initialize players and state.

        Returns:
            dict: first state in one game
            int: current player's id
        '''
        # initialize public variables
        self.final_score = [0, 0]
        self.winner_id = None
        #self.history = []

        # initialize players
        self.player_hands = [[], []]
        self.player_public_cards = [[], []]
        self.player_private_cards = [[], []]
        
        # initialize dealer
        self.dealer = SwyBlmDealer(self.np_random)
        
        # initialize board and player hands
        self.board_public_cards = self.dealer.draw_cards(2)
        
        self.player_hands[0] += self.dealer.draw_cards(4)  # first-hand player also draw a card at the start
        self.player_hands[1] += self.dealer.draw_cards(3)
        
        self.current_player = 0
        self.current_turn = 0   # exactly 12 turns in total

        # get state of first player
        self.current_state = self.get_state(self.current_player)

        return self.current_state, self.current_player

    def step(self, action):
        ''' Perform one draw of the game

        Args:
            action (str): specific action of doudizhu. Eg: '33344'

        Returns:
            dict: next player's state
            int: next player's id
        '''
        card, sec = action[:2], int(action[2])
        
        assert(card in self.player_hands[self.current_player])
        self.player_hands[self.current_player].remove(card)
        
        if sec == 0:  # put in private
            self.player_private_cards[self.current_player].append(card)
        else:  # put in public
            self.player_public_cards[self.current_player].append(card)
            
        # switch turn
        self.current_player = int(1 - self.current_player)
        self.current_turn += 1
        
        # draw a card
        self.player_hands[self.current_player] += self.dealer.draw_cards(1)

        self.current_state = self.get_state(self.current_player)
        return self.current_state, self.current_player

    def step_back(self):
        ''' Return to the previous state of the game

        Returns:
            (bool): True if the game steps back successfully
        '''
        
        raise NotImplementedError
        
#         if not self.round.trace:
#             return False

#         #winner_id will be always None no matter step_back from any case
#         self.winner_id = None

#         #reverse round
#         player_id, cards = self.round.step_back(self.players)

#         #reverse player
#         if (cards != 'pass'):
#             self.players[player_id].played_cards = self.round.find_last_played_cards_in_trace(player_id)
#         self.players[player_id].play_back()

#         #reverse judger.played_cards if needed
#         if (cards != 'pass'):
#             self.judger.restore_playable_cards(player_id)

#         self.state = self.get_state(self.round.current_player)
#         return True

    @staticmethod
    def compute_legal_actions(hand, public_count, private_count):
        actions = []
        if public_count < 3:
            actions += [card + '1' for card in hand]
        if private_count < 3:
            actions += [card + '0' for card in hand]
            
        return actions
    
    def judge_winner(self):
        public_cards = self.board_public_cards.copy()
        for player_id in range(self.num_players):
            public_cards += self.player_public_cards[player_id]
            
        for player_id in range(self.num_players):
            table, joker = _cards2table(public_cards + self.player_private_cards[player_id])
            
            score = 0
            
            for suit_id in range(4):  # 4, 8 points for Mei, Lan, Zhu, and Ju
                suit_count = table[:, suit_id].sum()
                score += (suit_count == 5) * 8 + (suit_count == 4) * 4
            
            for color_id in range(3):  # 1, 3 points for Grey, Blue, and Yellow
                color_count = table[color_id, :].sum()
                score += (color_count == 4) * 3 + (color_count == 3) * 1

            for color_id in range(3, 5):  # 3, 6 points for Colorful, and Red
                color_count = table[color_id, :].sum()
                score += (color_count == 4) * 6 + (color_count == 3) * 3
            
            score += (joker.sum() == 2) * 5  # 5 points for two jokers
            
            self.final_score[player_id] = score
            
        return np.argmax(self.final_score)

    def get_state(self, player_id):
        ''' Return player's state

        Args:
            player_id (int): player id

        Returns:
            (dict): The state of the player
        '''
        opponent_id = int(1 - player_id)
        
        state = {}
        state['player_id'] = player_id
        state['cur_hand'] = self.player_hands[player_id].copy()
        state['cur_turn'] = self.current_turn
        
        state['board_public'] = self.board_public_cards.copy()
        state['cur_public'] = self.player_public_cards[player_id].copy()
        state['cur_private'] = self.player_private_cards[player_id].copy()
        state['oppo_public'] = self.player_public_cards[opponent_id].copy()
        state['oppo_private_count'] = len(self.player_private_cards[opponent_id])
        
        return state

    def get_num_actions(self):
        ''' Return the total number of abstract acitons

        Returns:
            int: the total number of abstract actions of swy_blm
        '''
        return self.num_actions
    
    def get_player_id(self):
        ''' Return current player's id
        Returns:
            int: current player's id
        '''
        return self.current_player

    def get_num_players(self):
        ''' Return the number of players in swy_blm

        Returns:
            int: the number of players in swy_blm
        '''
        return self.num_players

    def is_over(self):
        ''' Judge whether a game is over

        Returns:
            Bool: True(over) / False(not over)
        '''
        if self.winner_id is not None:
            return True
        
        if self.current_turn == 12:
            self.winner_id = self.judge_winner()
            return True
        
        else:
            return False

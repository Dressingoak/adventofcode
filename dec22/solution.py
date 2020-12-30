from collections import deque
import logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

class Combat:

    logger = logging.getLogger('Combat')

    def __init__(self, player1: deque[int], player2: deque[int]):
        self.player1 = player1
        self.player2 = player2
        self.rounds = 0
        self.score = None

    def play_round(self):
        self.rounds += 1
        self.logger.debug("-- Round {} --".format(self.rounds))
        self.logger.debug("Player 1's deck: {}".format(", ".join([str(_) for _ in self.player1])))
        self.logger.debug("Player 2's deck: {}".format(", ".join([str(_) for _ in self.player2])))
        p1 = self.player1.popleft()
        p2 = self.player2.popleft()
        self.logger.debug("Player 1 plays: {}".format(p1))
        self.logger.debug("Player 2 plays: {}".format(p2))
        if p1 > p2:
            self.logger.debug("Player 1 wins the round!")
            self.player1.append(p1)
            self.player1.append(p2)
        elif p2 > p1:
            self.logger.debug("Player 2 wins the round!")
            self.player2.append(p2)
            self.player2.append(p1)
        else:
            raise Exception("No rules for a tie")

    def calculate_scores(self):
        return (
            sum((i+1)*v for i, v in enumerate(reversed(self.player1))),
            sum((i+1)*v for i, v in enumerate(reversed(self.player2)))
        )

    def play_game(self):
        while len(self.player1) > 0 and len(self.player2) > 0:
            self.play_round()
            self.logger.debug("")
        
        self.logger.debug("== Post-game results ==")
        self.logger.debug("Player 1's deck: {}".format(", ".join([str(_) for _ in self.player1])))
        self.logger.debug("Player 2's deck: {}".format(", ".join([str(_) for _ in self.player2])))
        (p1, p2) = self.calculate_scores()
        if p1 == 0:
            self.score = p2
            self.logger.debug("Player 2's score: {}".format(p2))
        elif p2 == 0:
            self.score = p1
            self.logger.debug("Player 1's score: {}".format(p1))
        else:
            raise Exception("One of the two scores show be zero, got {} and {} for player 1 and player 2, respectively.".format(p1, p2))

class RecursiveCombat:

    game_counter = 0
    logger = logging.getLogger('RecursiveCombat')

    def __init__(self, player1: deque[int], player2: deque[int], subgame_of = None):
        self.player1 = player1
        self.player2 = player2
        self.rounds = 0
        RecursiveCombat.game_counter += 1
        self.game = self.game_counter
        self.subgame_of = subgame_of
        self.score = None
        self.winner = None
        self.logger.debug("=== Game {} ===".format(self.game))
        self.past = set()
        self.record_decks()

    def record_decks(self):
        self.past.add((tuple(self.player1), tuple(self.player2)))

    def play_round(self):
        self.rounds += 1
        self.logger.debug("")
        self.logger.debug("-- Round {} (Game {}) --".format(self.rounds, self.game))
        self.logger.debug("Player 1's deck: {}".format(", ".join([str(_) for _ in self.player1])))
        self.logger.debug("Player 2's deck: {}".format(", ".join([str(_) for _ in self.player2])))
        p1 = self.player1.popleft()
        p2 = self.player2.popleft()
        self.logger.debug("Player 1 plays: {}".format(p1))
        self.logger.debug("Player 2 plays: {}".format(p2))
        if p1 <= len(self.player1) and p2 <= len(self.player2):
            self.logger.debug("Playing a sub-game to determine the winner...")
            self.logger.debug("")
            subgame = RecursiveCombat(
                deque([self.player1[i] for i in range(p1)]),
                deque([self.player2[i] for i in range(p2)]),
                self.game
            )
            winner = subgame.play_game()
            self.logger.debug("...anyway, back to game {}.".format(self.game))
        else:
            winner = 0 if p1 > p2 else 1
        if winner == 0:
            self.logger.debug("Player 1 wins round {} of game {}!".format(self.rounds, self.game))
            self.player1.append(p1)
            self.player1.append(p2)
        else:
            self.logger.debug("Player 2 wins round {} of game {}!".format(self.rounds, self.game))
            self.player2.append(p2)
            self.player2.append(p1)
        self.record_decks()

    def calculate_scores(self):
        return (
            sum((i+1)*v for i, v in enumerate(reversed(self.player1))),
            sum((i+1)*v for i, v in enumerate(reversed(self.player2)))
        )

    def play_game(self):
        recursion = False
        while (len(self.player1) > 0 and len(self.player2) > 0):
            if self.rounds + 1 != len(self.past):
                self.logger.debug("Infinite game recursion, player 1 wins game {}!".format(self.game))
                recursion = True
                break
            self.play_round()
        if not recursion:
            (p1, p2) = self.calculate_scores()
            if p1 == 0:
                self.winner = 1
                self.score = p2
            elif p2 == 0:
                self.winner = 0
                self.score = p1
            else:
                raise Exception("One of the two scores show be zero, got {} and {} for player 1 and player 2, respectively.".format(p1, p2))
        else:
            self.winner = 0
        self.logger.debug("The winner of game {} is player {}!".format(self.game, self.winner+1))
        self.logger.debug("")
        
        if self.subgame_of is None:
            self.logger.debug("")
            self.logger.debug("== Post-game results ==")
            self.logger.debug("Player 1's deck: {}".format(", ".join([str(_) for _ in self.player1])))
            self.logger.debug("Player 2's deck: {}".format(", ".join([str(_) for _ in self.player2])))
        return self.winner

decks = []
for lines in open("input.txt").read().strip().split("\n\n"):
    decks.append(deque([int(_) for _ in lines.strip().split("\n")[1:]]))

Combat.logger.propagate = False
game = Combat(decks[0].copy(), decks[1].copy())
game.play_game()
logging.info("Part 1: {}".format(game.score))

RecursiveCombat.logger.propagate = False
recursive_game = RecursiveCombat(decks[0].copy(), decks[1].copy())
recursive_game.play_game()
logging.info("Part 2: {}".format(recursive_game.score))

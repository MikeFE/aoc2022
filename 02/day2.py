""" https://adventofcode.com/2022/day/2 """

def get_sign_from_letter(letter):
    letters = {'A': 'rock', 'B': 'paper', 'C': 'scissors'}
    return letters[letter]

def get_outcome_from_letter(letter):
    letters = {'X': 'loss', 'Y': 'draw', 'Z': 'win'}
    return letters[letter]

def get_naive_score(their_move, your_move):
    """ Return integer score based on outcome using the naive strategy of
        X = Rock, Y = Paper, Z = Scissors, with scores:

        Loss = +0
        Draw = +3
        Win = +6
    """

    # Which signs defeat other signs, from both players' perspectives, used in evaluating outcome
    outcomes = {'A': 'Z', 'B': 'X', 'C': 'Y',
                'X': 'C', 'Y': 'A', 'Z': 'B'}

    equivalents = {'A': 'X', 'B': 'Y', 'C': 'Z'}

    if outcomes[their_move] == your_move:
        return 0  # you lose
    elif outcomes[your_move] == their_move:
        return 6  # you win
    elif equivalents[their_move] == your_move:
        return 3  # draw
    else:
        raise Exception(f'Unknown evaluation: {your_move} vs. {their_move}')

def get_decrypted_score(their_move, your_move):
    """ Get whether to lose, draw or win from your_move (X, Y, Z), then use appropriate move.

        Returns the total score gained given the outcome and which sign had to be used to get the
        desired outcome.
    """
    # first tuple element is what index in the sign_to_use_for_outcome map to use to get the result,
    # second tuple element is the score to add due to the outcome received.
    decrypted_map = {'X': (0, 0), 'Y': (1, 3), 'Z': (2, 6)}
    sign_scores = {'A': 1, 'B': 2, 'C': 3}

    sign_to_use_for_outcome = {  # Map indicating sign_they_used: (loss_sign, draw_sign, win_sign)
        'A': ('C', 'A', 'B'),
        'B': ('A', 'B', 'C'),
        'C': ('B', 'C', 'A')
    }

    sign_for_outcome = sign_to_use_for_outcome[their_move][decrypted_map[your_move][0]]
    result = sign_scores[sign_for_outcome] + decrypted_map[your_move][1]

    print(f'Got {get_sign_from_letter(their_move)} ({their_move}), playing {get_sign_from_letter(sign_for_outcome)} ({sign_for_outcome}) for result {get_outcome_from_letter(your_move)} ({your_move}) = {result}')
    return result

def eval_round(their_move, your_move, strategy_naive):
    """ Evaluates score for the round.

    their_move - 'A', 'B' or 'C' denoting rock, paper and scissors respectively
    your_move - 'X', 'Y', 'Z' denoting what your move ought to be given the strategy

    strategy_naive - if True take X, Y and Z to indicate moves of rock, paper and scissors
                     respectively. If False, take X, Y and Z to mean do the sign that
                     loses, draws or wins respectively.

    Returns int value representing how many points you won for the round.

    Depending what sign you chose adds to score as well:
        (X) Rock = +1
        (Y) Paper = +2
        (Z) Scissors = +3
    """
    sign_scores = {'X': 1, 'Y': 2, 'Z': 3}  # If x, y, z means rock, paper, scissors

    if strategy_naive:
        return get_naive_score(their_move, your_move) + sign_scores[your_move]
    else:
        return get_decrypted_score(their_move, your_move)

def main():
    rounds = []

    with open('day2.input.txt') as f:
        for ln in f.readlines():
            rounds.append(ln.rstrip().split(' '))  # remove newline, add list containing moves

    total_score = 0
    for round in rounds:
        total_score += eval_round(*round, True)

    print(f'Total score (naive strategy): {total_score}')

    total_score = 0
    for round in rounds:
        total_score += eval_round(*round, False)

    print(f'Total score (decrypted strategy): {total_score}')

if __name__ == '__main__':
    main()
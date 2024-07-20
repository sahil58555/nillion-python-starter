from nada_dsl import *

def initialize_bettors(nr_bettors):
    """
    Initializes the list of bettors with unique identifiers.

    Args:
    nr_bettors (int): Number of bettors.

    Returns:
    list: List of Party objects representing each bettor.
    """
    bettors = []
    for i in range(nr_bettors):
        bettors.append(Party(name="Bettor" + str(i)))

    return bettors

def inputs_initialization(nr_bettors, nr_events, bettors, outparty):
    """
    Initializes the input for each bet, odds, and user authentication.

    Args:
        nr_bettors (int): Number of bettors.
        nr_events (int): Number of events.
        bettors (list): List of Party objects representing each bettor.
        outparty (Party): The party responsible for the output.

    Returns:
        tuple: (bets, odds, user_auth, cancellation_deadline)
            - bets: List of lists containing SecretUnsignedInteger objects for bets.
            - odds: List of SecretUnsignedInteger objects for odds.
            - user_auth: List of SecretUnsignedInteger objects for user authentication.
            - cancellation_deadline: SecretUnsignedInteger object for cancellation deadline.
    """
    bets = [[SecretUnsignedInteger(Input(name=f"b{i}_e{j}", party=bettors[i])) for j in range(nr_events)] for i in range(nr_bettors)]
    odds = [SecretUnsignedInteger(Input(name=f"odds_e{j}", party=outparty)) for j in range(nr_events)]
    user_auth = [SecretUnsignedInteger(Input(name=f"auth_bettor_{i}", party=bettors[i])) for i in range(nr_bettors)]
    cancellation_deadline = SecretUnsignedInteger(Input(name="cancellation_deadline", party=outparty))

    return bets, odds, user_auth, cancellation_deadline

def compute_totals_and_payouts(nr_bettors, nr_events, bets, odds):
    """
    Computes the total bets for each event and the payouts.

    Args:
        nr_bettors (int): Number of bettors.
        nr_events (int): Number of events.
        bets (list): List of lists containing SecretUnsignedInteger objects for bets.
        odds (list): List of SecretUnsignedInteger objects for odds.

    Returns:
        tuple: (total_bets, payouts)
            - total_bets: List of SecretUnsignedInteger objects representing total bets for each event.
            - payouts: List of SecretUnsignedInteger objects representing payouts for each event.
    """
    total_bets = []
    payouts = []

    for j in range(nr_events):
        # Initialize the total bet for the event
        event_total_bet = SecretUnsignedInteger(Input(name=f"total_bet_event_{j}", party=Party(name=f"Internal")))
        for i in range(nr_bettors):
            # Using method to add SecretUnsignedInteger
            event_total_bet = event_total_bet + bets[i][j]
        
        total_bets.append(event_total_bet)
        payouts.append(event_total_bet * odds[j])

    return total_bets, payouts

def nada_main():
    # 0. Compiled-time constants
    nr_bettors = 3
    nr_events = 4

    # 1. Parties initialization
    bettors = initialize_bettors(nr_bettors)
    outparty = Party(name="OutParty")

    # 2. Inputs initialization
    bets, odds, user_auth, cancellation_deadline = inputs_initialization(nr_bettors, nr_events, bettors, outparty)

    # 3. Computation
    total_bets, payouts = compute_totals_and_payouts(nr_bettors, nr_events, bets, odds)

    # 4. Output
    outputs = []
    for j in range(nr_events):
        total_bets_output = Output(total_bets[j], f"total_bets_event_{j}", outparty)
        payouts_output = Output(payouts[j], f"payout_event_{j}", outparty)
        outputs.extend([total_bets_output, payouts_output])

    return outputs

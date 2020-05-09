import argparse
from collections import Counter
import pprint
import random
import sys

from tabulate import tabulate

SEASON_EPISODES = {1: 24, 2: 24, 3:25, 4:24, 5:24, 6:25, 7:24, 8:24, 9:24, 10:18}
SEASONS = range(1, 10+1)

FRIENDS = ["Ross", "Rachel", "Joey", "Chandler", "Monica", "Phoebe"]

def assign_watch_characters(friends=FRIENDS):
    selected_watch_target = []
    watch_pairs = {}

    for friend in set(friends):
        to_watch = random.choice(list(set(friends) - set([friend]+selected_watch_target)))
        selected_watch_target.append(to_watch)
        watch_pairs[friend] = to_watch

    return watch_pairs

def select_characters(players_list, friends=FRIENDS):
    num_players = len(players_list)
    num_characters = len(friends)

    char_list_multiplier = int(round((num_players/num_characters), 0)) + 1
    friends = friends * char_list_multiplier

    chosen_char_index = (random.sample(range(0, len(friends)), len(players_list)))
    chosen_characters = list(map(lambda x: friends[x], chosen_char_index))

    assigned_watch_pairs = assign_watch_characters(friends)

    print("-----Character Stats-----")
    char_counts = Counter(chosen_characters)
    char_stats = [[char, char_counts[char]] for char in char_counts.keys()]
    print(tabulate(char_stats, headers=["Character", "Number of players assigned"]))
    print("\n-----Assigned characters-----")
    assigned_players = [[player.capitalize(), chosen_characters[e], assigned_watch_pairs[chosen_characters[e]]] for e, player in enumerate(players_list)]
    print(tabulate(assigned_players, headers=["Player Name", "Character assigned", "Character to watch"]))


def select_episode(exclude_list=None, seasons=SEASONS):
    if exclude_list:
        seasons = list(set(seasons) - set(exclude_list))

    season_selected = random.choice(seasons)
    episode_selected = random.choice(range(1, SEASON_EPISODES[season_selected]+1))
    print("\n-----Show selected-----")
    print(f'Season {season_selected} Episode {episode_selected}')

def parse_season_arg(arg):
    if arg:
        return list(map(int, arg.split(",")))

    return arg


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--players')
    parser.add_argument('--pick_characters', action='store_true')
    parser.add_argument('--pick_episode', action='store_true')
    parser.add_argument('--pick_all', action='store_true')
    parser.add_argument('--exclude_seasons', default=None, type=parse_season_arg)
    parser.add_argument('--rand_seed', default=30)

    args = vars(parser.parse_args())

    random.seed(args['rand_seed'])

    players = args['players'].split(",")

    if all([args[arg] is False for arg in args if arg.startswith('pick_')]):
        sys.exit('All toggles off - Must pick either players, episode or all')

    if args['pick_characters'] or args['pick_all']:
        select_characters(players)

    if args['pick_episode'] or args['pick_all']:
        select_episode(args['exclude_seasons'])
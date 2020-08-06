import pandas as pd
import numpy as np
import random
from civ_random.generate_random_sets import generate_random_sets

def load_rating(ncivs: int, bans):
    rating = pd.read_csv('civ_random/rating.csv')
    cols = rating.columns

    for col in cols[1:]:
        for i in range(len(rating[col])):
            try:
                rat_val = rating[col].loc[i]
                rat_val = rat_val.replace(" ", "").split(sep = ',')
                rating[col].loc[i] = np.average([int(x) for x in rat_val])
            except ValueError:
                print('Incorrect value. Please, check the table.')

    total_rat = []

    for i in range(len(rating[cols[0]])):
        total_rat.append(
                rating[cols[1]].loc[i] +
                rating[cols[2]].loc[i] +
                2 * rating[cols[3]].loc[i] +
                rating[cols[4]].loc[i]
        )

    rating['AVERAGE'] = total_rat
    rating = rating[~rating['Нація'].isin(bans)]
    rating = rating.sort_values(by=['AVERAGE'], ascending=False).reset_index(drop=True)
    return rating

def get_split_indices_from_probs(probs, length):
    indices = [0]
    cur_ind = 0
    for p in probs:
        cur_ind += int(length * p)
        indices.append(cur_ind)
    indices[-1] += 1

    return indices

def balanced_random(pl_num:int, ncivs:int, bans):
    rand_civs = [[] for i in range(pl_num)]
    rating = load_rating(ncivs, bans)
    player_points = np.sum(np.arange(ncivs + 1))
    tier_sets, tier_probs, tiers = generate_random_sets(np.arange(1, ncivs + 1), ncivs, sum=player_points)
    split_inds = get_split_indices_from_probs(tier_probs, len(rating))

    for player in rand_civs:
        player_tier_set = random.choice(tier_sets)
        for tier in player_tier_set:
            rand_df = rating.loc[split_inds[tier-1]:split_inds[tier]]
            print(split_inds[tier-1],split_inds[tier])
            print(rand_df)
            nation = rand_df.sample(n=1)
            player.append(nation['Нація'].values[0] + '.jpg')
            rating = rating.drop(index = nation.index)

    return rand_civs



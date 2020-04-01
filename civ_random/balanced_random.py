import pandas as pd
import numpy as np

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
    rating = rating.sort_values(by=['AVERAGE'])
    rating = rating[~rating['Нація'].isin(bans)]
    rat_group = np.array_split(rating, ncivs)

    for i in range(len(rat_group)):
        rat_group[i]['POINTS'] = [i+1 for el in range(rat_group[i].shape[0])]

    return(pd.concat(rat_group))

def balanced_random(pl_num:int, ncivs:int, bans):
    rand_civs = [[] for i in range(pl_num)]
    rating = load_rating(ncivs, bans)

    for player in rand_civs:
        to_random = ncivs
        player_points = np.sum(np.arange(ncivs + 1))

        while to_random:
            if to_random == 1:
                rand_df = rating[
                    (rating['POINTS'].values <= player_points) &
                    (rating['POINTS'].values >= player_points // to_random)
                    ]
                nation = rand_df.sample(n=1)
                rating = rating.drop(nation.index)
                player.append(nation['Нація'].values[0] + '.jpg')
                to_random -= 1

            else:
                # print(player_points-to_random+1)
                rand_df = rating[
                    (rating['POINTS'].values <= player_points-to_random+1) &
                    (rating['POINTS'].values >= player_points//to_random)
                ]
                nation = rand_df.sample(n=1)
                rating = rating.drop(nation.index)
                player.append(nation['Нація'].values[0] + '.jpg')
                to_random -= 1
                player_points -= nation['POINTS'].values[0]

    return rand_civs



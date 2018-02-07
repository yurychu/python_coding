from math import sqrt


critics = {
    'Lisa Rose': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 3.5,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 3.0
    },
    'Gene Seymour': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 1.5,
        'Superman Returns': 5.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 3.5
    },
    'Michael Phillips': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.0,
        'Superman Returns': 3.5,
        'The Night Listener': 4.0
    },
    'Claudia Puig': {
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'The Night Listener': 4.5,
        'Superman Returns': 4.0,
        'You, Me and Dupree': 2.5
    },
    'Mick LaSalle': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'Just My Luck': 2.0,
        'Superman Returns': 3.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 2.0
    },
    'Jack Matthews': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'The Night Listener': 3.0,
        'Superman Returns': 5.0,
        'You, Me and Dupree': 3.5
    },
    'Toby': {
        'Snakes on a Plane': 4.5,
        'You, Me and Dupree': 1.0,
        'Superman Returns': 4.0
    }
}


def transform_prefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            result[item][person] = prefs[person][item]
    return result


def sim_distance(prefs, person1, person2):
    """
    :param prefs:
    :param person1:
    :param person2:
    :return: bigger - similarly, 1 - equal
    """
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    if len(si) == 0:
        return 0

    sum_of_squares = sum(
        [
            pow(prefs[person1][item] - prefs[person2][item], 2) for item in prefs[person1] if item in prefs[person2]
        ]
    )
    return 1 / (1 + sum_of_squares)


def sim_pearson(prefs, p1, p2):
    """
    :param prefs:
    :param p1:
    :param p2:
    :return: from -1 to 1, 1 - similarly
    """
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1

    n = len(si)
    if n == 0:
        return 0

    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum(prefs[p2][it] for it in si)

    sum1_sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2_sq = sum([pow(prefs[p2][it], 2) for it in si])

    p_sum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    num = p_sum - (sum1 * sum2 / n)
    den = sqrt(
        (sum1_sq - pow(sum1, 2) / n) * (sum2_sq - pow(sum2, 2) / n)
    )
    if den == 0:
        return 0

    return num / den


def top_matches(prefs, person, n=5, similarity=sim_pearson):
    scores = [
        (similarity(prefs, person, other), other) for other in prefs if other != person
    ]
    scores.sort()
    scores.reverse()
    return scores[0:n]


def get_recommedations(prefs, person, similarity=sim_pearson):
    totals = {}
    sim_sums = {}

    for other in prefs:
        if other == person:
            continue

        sim = similarity(prefs, person, other)
        if sim <= 0:
            continue

        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                sim_sums.setdefault(item, 0)
                sim_sums[item] += sim

    rankings = [(total / sim_sums[item], item) for item, total in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings


points = {
    "1": {
        "seq": 20,
        "x": 551,
        "y": 103,
    },
    "2": {
        "seq": 21,
        "x": 541,
        "y": 119,
    },
}


if __name__ == "__main__":
    print(
        top_matches(transform_prefs(critics), "Superman Returns")
    )


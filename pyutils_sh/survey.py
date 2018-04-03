"""
Functions for aggregating and analyzing different types of survey data.
"""

import numpy as np
import pandas as pd


def ipaq_long_aggregate(q_map):
    # Check that the map contains all 42 IPAQ long questions
    if len(q_map) != 42:
        raise Exception("Please map all 42 IPAQ (long form) questions (41 "
                        "questions + 1 subject number column). Refer to "
                        "documentation for mapping rules.")

    df = pd.DataFrame(q_map)

    return df


def convert_IPAQ_time(time_column, truncate=False, sit="none"):
    """ Addresses 7.1.I of the scoring protocol """

    orig_time = time_column.fillna(0).astype(str)
    converted = pd.Series().astype(float)

    for row in orig_time.iteritems():
        time = row[1]

        if ":" in time:
            hours, mins, secs = map(float, time.split(":"))

            # Check for out of bound hour values and add to minutes value
            if hours in [15, 30, 45, 60, 90]:
                mins += hours
                hours = 0

            # Convert time to minutes
            converted.loc[converted.shape[0]] = (hours*60) + mins
        else:
            converted.loc[converted.shape[0]] = float(time)  # Time already in minutes

    # Scoring protocol 7.3 - at least 10 minutes of activity
    converted[converted < 10] = 0

    # Scoring protocol 7.4 - truncate each to 180mins (as per SHORT form protocol)
    if truncate:
        converted[converted > 180] = 180

    if sit == "weekday":
        converted[converted > 1440] = converted[converted > 1440]/5
    elif sit == "weekend":
        converted[converted > 1440] = converted[converted > 1440]/2

    return converted

def calculate_IPAQ(data):
    q2 = data["2. During the last 7 days, on how many days did you do vigorous physical activities like heavy lifting, digging, heavy construction, or climbing up stairs as part of your work? Think about only those physical activities that you did for at least 10 minutes at a time."].fillna(0).apply(float)
    q3 = convert_IPAQ_time(data["3. How much time did you usually spend on one of those days doing vigorous physical activities as part of your work?"], True)
    q4 = data["4. Again, think about only those physical activities that you did for at least 10 minutes at a time. During the last 7 days, on how many days did you do moderate physical activities like carrying light loads as part of your work? Please do not include walking."].fillna(0).apply(float)
    q5 = convert_IPAQ_time(data["5. How much time did you usually spend on one of those days doing moderate physical activities as part of your work?"], True)
    q6 = data["6. During the last 7 days, on how many days did you walk for at least 10 minutes at a time as part of your work? Please do not count any walking you did to travel to or from work."].fillna(0).apply(float)
    q7 = convert_IPAQ_time(data["7. How much time did you usually spend on one of those days walking as part of your work?"], True)
    q10 = data["10. During the last 7 days, on how many days did you bicycle for at least 10 minutes at a time to go from place to place?"].fillna(0).apply(float)
    q11 = convert_IPAQ_time(data["11. How much time did you usually spend on one of those days to bicycle from place to place?"], True)
    q12 = data["12. During the last 7 days, on how many days did you walk for at least 10 minutes at a time to go from place to place?"].fillna(0).apply(float)
    q13 = convert_IPAQ_time(data["13. How much time did you usually spend on one of those days walking from place to place?"], True)
    q14 = data["14. Think about only those physical activities that you did for at least 10 minutes at a time. During the last 7 days, on how many days did you do vigorous physical activities like heavy lifting, chopping wood, shoveling snow, or digging in the garden or yard?"].fillna(0).apply(float)
    q15 = convert_IPAQ_time(data["15. How much time did you usually spend on one of those days doing vigorous physical activities in the garden or yard?"], True)
    q16 = data["16. Again, think about only those physical activities that you did for at least 10 minutes at a time. During the last 7 days, on how many days did you do moderate activities like carrying light loads, sweeping, washing windows, and raking in the garden or yard?"].fillna(0).apply(float)
    q17 = convert_IPAQ_time(data["17. How much time did you usually spend on one of those days doing moderate physical activities in the garden or yard?"], True)
    q18 = data["18. Once again, think about only those physical activities that you did for at least 10 minutes at a time. During the last 7 days, on how many days did you do moderate activities like carrying light loads, washing windows, scrubbing floors and sweeping inside your home?"].fillna(0).apply(float)
    q19 = convert_IPAQ_time(data["19. How much time did you usually spend on one of those days doing moderate physical activities inside your home?"], True)
    q20 = data["20. Not counting any walking you have already mentioned, during the last 7 days, on how many days did you walk for at least 10 minutes at a time in your leisure time?"].fillna(0).apply(float)
    q21 = convert_IPAQ_time(data["21. How much time did you usually spend on one of those days walking in your leisure time?"], True)
    q22 = data["22. Think about only those physical activities that you did for at least 10 minutes at a time. During the last 7 days, on how many days did you do vigorous physical activities like aerobics, running, fast bicycling, or fast swimming in your leisure time?"].fillna(0).apply(float)
    q23 = convert_IPAQ_time(data["23. How much time did you usually spend on one of those days doing vigorous physical activities in your leisure time?"], True)
    q24 = data["24. Again, think about only those physical activities that you did for at least 10 minutes at a time. During the last 7 days, on how many days did you do moderate physical activities like bicycling at a regular pace, swimming at a regular pace, and doubles tennis in your leisure time?"].fillna(0).apply(float)
    q25 = convert_IPAQ_time(data["25. How much time did you usually spend on one of those days doing moderate physical activities in your leisure time?"], True)

    # Sitting variables - don't truncate to 180mins
    q26 = convert_IPAQ_time(data["26. During the last 7 days, how much time did you usually spend sitting on a weekday?"], False, "weekday")
    q27 = convert_IPAQ_time(data["27. During the last 7 days, how much time did you usually spend sitting on a weekend day?"], False, "weekend")

    # Work domain
    work_walk_time = q6 * q7
    work_walk_MET = 3.3 * work_walk_time

    work_mod_time = q4 * q5
    work_mod_MET = 4.0 * work_mod_time

    work_vig_time = q2 * q3
    work_vig_MET = 8.0 * work_vig_time

    work_total_time = work_walk_time + work_mod_time + work_vig_time
    work_total_MET = work_walk_MET + work_mod_MET + work_vig_MET

    # Active transportation domain
    transport_walk_time = q12 * q13
    transport_walk_MET = 3.3 * transport_walk_time

    transport_cycle_time = q10 * q11
    transport_cycle_MET = 6.0 * transport_cycle_time

    transport_total_time = transport_walk_time + transport_cycle_time
    transport_total_MET = transport_walk_MET + transport_cycle_MET

    # Domestic and garden (yard) domain
    domestic_vig_time = q14 * q15
    domestic_vig_MET = 5.5 * domestic_vig_time

    domestic_mod_yard_time = q16 * q17
    domestic_mod_yard_MET = 4.0 * domestic_mod_yard_time

    domestic_mod_inside_time = q18 * q19
    domestic_mod_inside_MET = 3.0 * domestic_mod_inside_time

    domestic_total_time = domestic_vig_time + domestic_mod_yard_time + domestic_mod_inside_time
    domestic_total_MET = domestic_vig_MET + domestic_mod_yard_MET + domestic_mod_inside_MET

    # Leisure domain
    leisure_walk_time = q20 * q21
    leisure_walk_MET = 3.3 * leisure_walk_time

    leisure_mod_time = q24 * q25
    leisure_mod_MET = 4.0 * leisure_mod_time

    leisure_vig_time = q22 * q23
    leisure_vig_MET = 8.0 * leisure_vig_time

    leisure_total_time = leisure_walk_time + leisure_mod_time + leisure_vig_time
    leisure_total_MET = leisure_walk_MET + leisure_mod_MET + leisure_vig_MET

    # Sitting behaviour
    sitting_total_time = (5.0 * q26) + (2.0 * q27)

    # Scoring protocol 7.2 - calculate extreme time values
    outliers = q3 + q5 + q7 + q11 + q13 + q15 + q17 + q19 + q21 + q23 + q25
    outliers[outliers <= 960] = 0
    outliers[outliers > 960] = 1

    # Total scores
    walk_total_time = work_walk_time + transport_walk_time + leisure_walk_time
    walk_total_MET = work_walk_MET + transport_walk_MET + leisure_walk_MET

    mod_total_time = work_mod_time + domestic_mod_yard_time + domestic_mod_inside_time + leisure_mod_time + transport_cycle_time + domestic_vig_time
    mod_total_MET = work_mod_MET + domestic_mod_yard_MET + domestic_mod_inside_MET + leisure_mod_MET + transport_cycle_MET + domestic_vig_MET

    vig_total_time = work_vig_time + leisure_vig_time
    vig_total_MET = work_vig_MET + leisure_vig_MET

    pa_total_time = work_total_time + transport_total_time + domestic_total_time + leisure_total_time
    pa_total_MET = work_total_MET + transport_total_MET + domestic_total_MET + leisure_total_MET

    # Calculate IPAQ categories

    walk_days = q6 + q12 + q20
    #walk_time_items = (q7, q13, q21)

    mod_days = q4 + q10 + q14 + q16 + q18 + q24
    #mod_time_items = (q5, q11, q15, q17, q19, q25)

    vig_days = q2 + q22
    #vig_time_items = (q3, q23)

    ## Low category
    category = pd.Series(np.ones(data.shape[0]))

    ## Moderate category
    days = pd.concat([q2, q22], axis = 1)
    times = pd.concat([q3, q23], axis = 1)
    category[(days.values * (times.values >= 20)).sum(1) >= 3] = 2

    days = pd.concat([q6, q12, q20, q4, q10, q14, q16, q18, q24], axis = 1)
    times = pd.concat([q7, q13, q21, q5, q11, q15, q17, q19, q25], axis = 1)
    category[(days.values * (times.values >= 30)).sum(1) >= 5] = 2

    mask = ((walk_days + mod_days + vig_days) >= 5) & (pa_total_MET >= 600)
    category[mask] = 2

    ## High category
    mask = (vig_days >= 3) & (vig_total_MET >= 1500)
    category[mask] = 3

    mask = ((walk_days + mod_days + vig_days) >= 7) & (pa_total_MET >= 3000)
    category[mask] = 3

    df = pd.DataFrame({"IPAQ_outlier": outliers,
                       "IPAQ_sitting_time": sitting_total_time,
                       "IPAQ_walk_time": walk_total_time,
                       "IPAQ_walk_MET": walk_total_MET,
                       "IPAQ_mod_time": mod_total_time,
                       "IPAQ_mod_MET": mod_total_MET,
                       "IPAQ_vig_time": vig_total_time,
                       "IPAQ_vig_MET": vig_total_MET,
                       "IPAQ_total_time": pa_total_time,
                       "IPAQ_total_MET": pa_total_MET,
                       "IPAQ_category": category
                       })

    # Set row to NA if summed time value is too extreme (outlier)
    df[df["IPAQ_outlier"] == 1] = np.NaN
    df = df.drop("IPAQ_outlier", 1)

    df["sub_num"] = data["Subject ID:"].astype(int)

    return df

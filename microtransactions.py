#!/usr/bin/env python3

import pandas as pd
from scipy.stats import chi2_contingency, binom_test 

df = pd.read_csv("clicks.csv")

is_purchase = []

for index, value in df["click_day"].notna().iteritems():
    if value == True:
        is_purchase.append("Purchase")
    else:
        is_purchase.append("No Purchase")

df["is_purchase"] = is_purchase

purchase_counts = df.groupby(["group", "is_purchase"])["user_id"].count()

a = list(purchase_counts)
contingency = [[a[1], a[0]],
               [a[3], a[2]],
               [a[5], a[4]]]

chi2, p, dof, expected = chi2_contingency(contingency)

num_of_visitors = df.shape[0]

# Calculate the number of people who would need to purchase a $0.99 upgrade in order to generate $1000.
a_people = 1000/.99

# Then divide by the number of people who visit the site each week.
percent_a = a_people / num_of_visitors

# Calculate the number of people who would need to purchase a $1.99 upgrade in order to generate $1000.
b_people = 1000/1.99

# Then divide by the number of people who visit the site each week.
percent_b = b_people / num_of_visitors

# Calculate the number of people who would need to purchase a $1.99 upgrade in order to generate $1000.
# Note: I believe this is a mistype, should be $4.99
c_people = 1000/4.99

# Then divide by the number of people who visit the site each week.
percent_c = c_people / num_of_visitors

# Test group A here
test_group_a = binom_test(a[1], a[1] + a[0], percent_a)

# Test group B here
test_group_b = binom_test(a[3], a[2] + a[3], percent_b)

# Test group C here
test_group_c = binom_test(a[5], a[4] + a[5], percent_c)

print("Test group C is the desired price point with p being less than .05")
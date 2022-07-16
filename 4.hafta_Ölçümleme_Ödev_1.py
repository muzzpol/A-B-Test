########################################################
# Comparison of Bidding Methods Conversion with AB Test
########################################################

##################
# Business Problem
##################

"""
Facebook, which has a bidding product called maximumbidding, has recently introduced
a product called averagebidding as an alternative to this product.
Our client bombabomba.com decided to test this new feature.
And they want to do an A/B test to see if averagebidding converts more than maximumbidding.
The A/B test has been going on for 1 month and bombabomba.com is now waiting for you to analyze
the results of this A/B test. The ultimate success criterion for Bombabomba.com is Purchase.
Therefore, the focus should be on the Purchase metric for statistical testing.
"""

##################
# Dataset Story
##################

"""
In this dataset, which includes the website information of a company, there is information such as 
the number of advertisements that users see and click, as well as earnings information from here.
There are two separate data sets, the control and test groups. These datasets are in separate sheets 
of the ab_testing.xlsx excel. Maximum Bidding was applied to the control group and AverageBidding 
was applied to the test group."""

"""
4 Variables         40 Observations         26KB

# Impression  :Ad views
# Click       :Number of clicks on the displayed ad
# Purchase    :Number of products purchased after ads clicked
# Earning     :Earnings after purchased products

"""

###############################
# Preparing and Analyzing Data
###############################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#!pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import shapiro, levene, ttest_ind
from statsmodels.stats.proportion import proportions_ztest
from statsmodels.stats.multicomp import MultiComparison

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.4f' % x)

#############################################################################################
# 1.1   Read the data set ab_testing_data.xlsx consisting of control and test group data.
#       Assign control and test group data to separate variables
#############################################################################################

C=pd.read_excel(r"C:\Users\mustafapolat\Desktop\Muzzpol\VBO\Python\Ölçümleme Problemleri\ab_testing_veri\ab_testing.xlsx",sheet_name="Control Group")
T=pd.read_excel(r"C:\Users\mustafapolat\Desktop\Muzzpol\VBO\Python\Ölçümleme Problemleri\ab_testing_veri\ab_testing.xlsx",sheet_name="Test Group")

#############################################################################################
# 1.2 Lets anaylze the control and test group data
#############################################################################################

C.describe().T
T.describe().T

def check_df(df, head=5, box=False, column="Purchase"):
    print("--------------------- Shape ---------------------")
    print(df.shape)
    print("---------------------- Types --------------------")
    print(df.dtypes)
    print("--------------------- Head ---------------------")
    print(df.head(head))
    print("--------------------- Quantiles ---------------------")
    print(df.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(C,box=True)
check_df(T,box=True)

#############################################################################################
# 1.3 We add group variable to both dataframes and concat them.
#############################################################################################
C["Group"]="C"
T["Group"]="T"
df= pd.concat([C,T],ignore_index=True)
df



###############################
# 2. Defining the A/B Test Hypotheses:
###############################

""" 
# We perform A/B testing in 3 steps.
# 1. Define hypotheses
# 2. Normality Assumption and Variance Homogeneity Control
# 3. Application of the Hypothesis
"""
#############################################################################################
# 2.1 Defining the A/B Test Hypotheses
#############################################################################################
# H0: M1 = M2   ==> There is no difference between test and control group's purchasing average
# H1: M1 != M2  ==> There is a difference between test and control group's purchasing average

#############################################################################################
# 2.2 Purchasing averages of control and test groups :
#############################################################################################

df.groupby("Group")["Purchase"].mean()

###############################
# 3.1 Performing Hypothesis Testing
###############################
"""
Perform hypothesis checks before hypothesis testing. These are Assumption of Normality 
and Homogeneity of Variance. Test separately whether the control and test groups comply 
with the assumption of normality over the Purchase variable.

Normality Assumption:

H0: Normal distribution assumption is provided.
H1: The assumption of normal distribution is not provided.
p < 0.05 H0 REJECT , p > 0.05 H0 CANNOT BE REJECTED.
Is the assumption of normality according to the test result provided for the control and test groups?
Interpret the p-values obtained.
"""
# Normality Assumption:

test_stat, pvalue = shapiro(df.loc[df["Group"] == "C", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 0.9773, p-value = 0.58914

test_stat, pvalue = shapiro(df.loc[df["Group"] == "T", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 0.9589, p-value = 0.1541

# H0 cannot be rejected since p value > 0.05 in both groups.
# The assumption of normal distribution is provided.


"""
Variance Homogeneity:

H0: Variances are homogeneous.
H1: Variances are not homogeneous.
p < 0.05 H0 RED ,
p > 0.05 H0 CANNOT BE REJECTED.
Test whether the homogeneity of variance is provided for the control and test groups over the Purchase variable.
Is the assumption of normality provided according to the test result?
Interpret the p-values obtained.

"""

# Variance Homogeneity:
# H0: Variances are homogeneous.
# H1: Variances are not homogeneous.

test_stat, pvalue = levene(df.loc[df["Group"] == "C", "Purchase"],
                           df.loc[df["Group"] == "T", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
    # Test Stat = 2.6393, p-value = 0.1083
    # H0 cannot be rejected because p value > 0.05.
    # Variances are homogeneous.

#############################################################################################
# 3.2 Let's choose the appropriate test according to the Normality Assumption and Variance Homogeneity results
#############################################################################################

    # We can use the t test. Because, we provided normality and homogeneity of variance
test_stat, pvalue = ttest_ind(df.loc[df["Group"] == "C", "Purchase"],
                              df.loc[df["Group"] == "T", "Purchase"],equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
    # Test Stat = -0.9416, p-value = 0.3493

#############################################################################################
# 3.3 Considering the p_value obtained as a result of the test,
# let's interpret whether there is a statistically significant difference between the purchasing averages of the control and test group.
#############################################################################################

    # H0 : M1 = M2
    # H1 : M1!= M2
    # p value > 0.05, the H0 hypothesis cannot be rejected.
    # There is no statistically significant difference between the purchase averages for the Control and Test groups,
    # with a 95% confidence interval and a 5% margin of error.

import pandas as pd
from matplotlib import pyplot as plt

#load the dataset
data = pd.read_csv('SingleCummulativeForEachConstraint_0_1011.csv')
# delete rows where flip is bigger than 500. WARNING: tilts the data
# data = data.drop(data.loc[data['flip'] > 500].index, axis=0)
print(data.describe())

#first, let's plot some stuff
data_grouped_by_n_constr = data.groupby(['numOfConstraints'])
means = data_grouped_by_n_constr.mean()

#plot developement of means
if False:
    for metric in ['loop']:#, 'backtrack', 'flip', 'unit']:
        plt.plot(means[metric], label='mean')
        plt.ylabel(metric+'s')
        plt.xlabel('number of constraints')
        plt.legend()
        plt.show()

# scatter plots
if False:
    for metric in ['loop', 'backtrack', 'flip', 'unit']:
        plt.scatter(data['numOfConstraints'], data[metric])
        plt.ylabel(metric + 's')
        plt.xlabel('number of constraints')
        plt.show()
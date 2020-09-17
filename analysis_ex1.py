import pandas
from pandas import DataFrame
from matplotlib import pyplot as plt

# set true if you want to plot stuff
plotting = False

# load the data
data = pandas.read_csv('results/solver_comparison.csv')

# group data by solver
grouped_data = data.groupby(by=['name'])
print(grouped_data)

# split data for easier comparison
loop_data = DataFrame(columns=['DLIS(True)', 'DLIS(False)', 'JW-OS', 'DLCS', 'HERO'],
                      index=range(1, int(len(data)/5)+1))
flip_data = DataFrame(columns=['DLIS(True)', 'DLIS(False)', 'JW-OS', 'DLCS', 'HERO'],
                      index=range(1, int(len(data)/5)+1))
backtrack_data = DataFrame(columns=['DLIS(True)', 'DLIS(False)', 'JW-OS', 'DLCS', 'HERO'],
                      index=range(1, int(len(data)/5)+1))
split_data = {'loop':loop_data, 'flip':flip_data, 'backtrack':backtrack_data}

# fill in the values
for key, _ in grouped_data:
    curr_group=grouped_data.get_group(key).set_index(['sudokuID'])

    loop_data[key] = curr_group['loop']
    flip_data[key] = curr_group['flip']
    backtrack_data[key] = curr_group['backtrack']

# plot boxplots
if plotting:
    for curr_data in split_data:
        df = split_data[curr_data]
        col = df.columns.values
        boxplot = df.boxplot(column=['DLIS(True)','DLIS(False)', 'JW-OS', 'DLCS', 'HERO'])
        plt.title(curr_data)
        plt.ylim(0, 1000)
        plt.show()


print(loop_data)
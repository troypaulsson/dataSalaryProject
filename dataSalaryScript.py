import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Read in the data
data = pd.read_csv('data_cleaned_2021.csv')

# Take a look at the data
print(data.head())
print(data.info())
print(data.columns)
print(data['Job Title'].value_counts())
print(data['Job Location'].value_counts())
print(data['Salary Estimate'][0:6])
# Shows descriptive statistics based on columns
print(data.describe())
# Shows the location and the company name of the first 6 entries
print(data[['Job Location','Company Name']][0:6])
# A different way to do the same thing
data.loc[0:5,['Job Location','Company Name']]
# Shows the company names, notice how each one has \n and then some numbers at the end
print(data['Company Name'])
# Gets rid of the \n and numbers for each company name
data['Company Name'] = data['Company Name'].apply(lambda x: x.replace("\n","    ").split("    ")[0])
print(data['Company Name'])
# Shows if there are any null values
print(data.isna().sum())





# Shows entries where the rating is -1
print(data[data['Rating']==-1])
# Replace the -1 values with nan value, and then replace that with the mean of the distribution
data['Rating'] = data['Rating'].apply(lambda x: np.nan if x == -1 else x)
data['Rating'] = data['Rating'].fillna(data['Rating'].mean())
# Check if values were successfully replaced
print(data[data['Rating']==-1])
 # Create a plot showing the distribution of ratings
sns.displot(data["Rating"],kde=True,color="red")
plt.title('Distribution of Rating Column\n', size=16, color='black')
plt.xlabel('Rating', fontsize=13, color='black')
plt.ylabel('Density', fontsize=13, color='black')
plt.tight_layout()
plt.show()





# Create a bar graph of the amount of jobs in each job location
fig, ax = plt.subplots(nrows=1,ncols=1)
sns.barplot(x=data['Job Location'].value_counts().index[0:10],y=data['Job Location'].value_counts()[0:10])
plt.title('States with Highest Percentage of Data Jobs',size=16,color='black')
plt.xlabel('State',size=13,color='black')
plt.ylabel('Count',size=13,color='black')
# Remove top and right borders
sns.despine(bottom=False,left=False)
# Add percentage at the top of each bar
spots = data["Job Location"].value_counts().index[0:10]
for p in ax.patches:
    ax.text(p.get_x() + 0.1, p.get_height()+4.5, '{:.2f}%'.format((p.get_height()/742)*100))
plt.tight_layout()
plt.show()




# Look at average minimal and maximal salaries in different states
# Create a dataframe with 3 columns, Job Location, lower salary and upper salary. Fill values with the mean by state.
salary = data.groupby('Job Location')['Lower Salary','Upper Salary'].mean().reset_index()
print(salary.head())
# Create a sorter based on the states with the highest number of jobs
sorter = data['Job Location'].value_counts().index
print(sorter)
# Converting Job Location column as category and setting the sorter
salary['Job Location'] = salary['Job Location'].astype('category')
salary['Job Location'].cat.set_categories(sorter, inplace=True)
print(salary.head())
# Resetting and dropping index
salary = salary.sort_values(['Job Location']).reset_index()
salary = salary.drop('index',axis=1)
print(salary.head())
# Drawing grouped bar plot
lab = []
for i in sorter[0:10]:
    lab.append(i)
x = np.arange(len(lab)) # label locations
width = 0.35            # width of bars
fig, ax = plt.subplots(1)
rects1 = ax.bar(x - width/2, salary['Lower Salary'][0:10], width, label='Min Salary')
rects2 = ax.bar(x + width/2, salary['Upper Salary'][0:10], width, label='Max Salary')

plt.title('Average Annual Minimal and Maximal Salaries by State', size=16, color='black')
plt.xlabel('States (Sorted by Amount of Jobs)', fontsize=13, color='black')
plt.ylabel('Salary (K)', fontsize=13, color='black')
ax.set_xticks(x)
ax.set_xticklabels(lab)
ax.legend()
plt.show()







# Create a pie chart showing the top 5 industries for data science jobs
my_explode = (0.1,0.1,0.1,0.1,0.1)
labels = [x for x in data["Industry"].value_counts().sort_values(ascending=False)[0:5].index] # piechart for only top 5 industry
patches,ax, text= plt.pie(data["Industry"].value_counts().sort_values(ascending=False)[0:5],autopct='%1.1f%%',explode=my_explode,shadow=True,startangle=300)
plt.title('Top 5 Industries with Most Number of Data Science Related Jobs', size=16, color='black')
plt.legend(patches, labels, loc="best")
plt.axis('equal')
plt.tight_layout()
plt.show()








# Import longitute and latitude information to work towards a visualization of job locations. Change name of State column to Job Location
latlong = pd.read_csv('statelatlong.csv').rename(columns={'State':'Job Location'})
#print(latlong.head())
# Drop city column as it is not needed
latlong = latlong.drop('City',axis=1)
# Merge the two dataframes by the Job Location column
data = data.merge(latlong, on='Job Location')
#print(data.head())

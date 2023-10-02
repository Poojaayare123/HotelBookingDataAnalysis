# For the analysis using sql, it would be better if you have the dataset in the database in different tables,
# so you can run different queries to get your meaningful insights.
# When you have not that spread data like 2 to 3 data files then using python and loading it into scripts and
# notebook would be good. And both are good when you need to get an answer.
# Power bi and tableau visualizations is important when you need to show the data in a meaningful form to anyone and
# don't need an answer to a particular business problem but just to see the data through out the time.


# How do you decide whether you want to analyze on python or SQL or via power bi or tableau?
# It depends what are you
# going to solve or for which problem you need to solution. If you need an answer then python would be best Sql+
# python when the data is stored in multiple table in database Need just to see how the data is working throughout
# the time, cities, demographics etc then you need to build the dashboard using power bi or tableau
#

# diff bet plots---https://www.youtube.com/watch?v=8U5h3EJuu8M&ab_channel=KimberlyFessel
# =========================================================================================================
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plot
import warnings

warnings.filterwarnings("ignore", "is_categorical_dtype")
warnings.filterwarnings("ignore", "use_inf_as_na")

df = pd.read_csv(r'C:\Users\pc\OneDrive\Desktop\DataAnalysisWithPythonHOtelbooking\hotel_booking.csv')
print(df)

# ---------------------------EDA-------------------------------------------------
# 1. Identifying the raw data
print(df.head(10))

print(df.tail(10))

print(df.shape)

print(df.columns)

# to check datatype of data here date is in object
print(df.info())

# ******************to convert into date  --pd.datetime()******************
df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])
print(df.info())

# **********To convert into other datatype*********************************
# .astype('int') used
# df['Amount'] = df['Amount'].astype('int')

# ********* describe()-It returns description of data of the Dataframe(i.e count,mean,unique values etc)
# To check how much categories present in object datatype
print(df.describe())

# *************************************Describe****************
# use only with numerical columns but when you want to use with object(categorical) datatype
# Then have to use include as below
print(df.describe(include='object'))

# To describe specific column
print(df[['reserved_room_type', 'country', 'credit_card']].describe())

# Find out all the columns of object datatype
# we will use above describe function with include which is giving data about objects
for col in df.describe(include='object').columns:
    print(col)
    print(df[col].unique())
    print('-' * 50)

# ********************Find out columns which have null values*********************
print(df.isnull().sum())  # children, company ,agent and meal is missing values in columns (no use of that columns)

# # ******************** Delete unused columns /rows ************************************
df.drop(['company', 'agent'], axis=1, inplace=True)
# axis == This parameter specifies whether to remove rows or columns. By default,
# 0=rows are removed
# 1=columns are removed
# inplace = It determines whether to modify the original DataFrame. By default, it is set to False.


# ********************** To delete null values *************************************
df.dropna(inplace=True)
print(df.isnull().sum())

# -------------Imp--------------- To show all columns in op set_option used
pd.set_option('display.max_columns', None)

# -----------Imp----------------- Outliers= values within a dataset that vary greatly from the others( eg adr column= 5400 value)
print(df.describe())

# Using Describe() get to know about adr outlier so will remove that
df = df[df['adr'] < 5000]
print(df.describe())

# *********** Analyzing cleaned data *************

# To check how many reservations got cancelled( in %)

# -------------------.value_counts(normalize=True)------------------
# returns a Series that contain counts of unique values. It returns an object that will be in descending order so that its first element will be the most frequently-occurred element.
# By default, it excludes NA values.
# normalize: If it is true, then the returned object will contain the relative frequencies of the unique values.
# sort: It sorts by the values.
# ascending: It sorts in the ascending order.
# bins: Rather than counting the values, it groups them into the half-open bins that provide convenience for the pd.cut, which only works with numeric data.
# dropna: It does not include counts of NaN.

cancelled_perc = df['is_canceled'].value_counts(normalize=True)  # 37% are cancelled reservations
print(cancelled_perc)

# # -------------Creating plot to show cancelled and not cancelled reservations---------
#
# plot.title('Reservation status count')
# # ax = sns.countplot(x='is_canceled', data=df)
#
# # for bars in ax.containers:
# #     ax.bar_label(bars)  # bar_label==Adds labels to bars in the given BarContainer .
# # plot.show()
#
# # ------------------or using bar plot-----------------------------
#
# plot.bar(['Not canceled', 'Canceled'], df['is_canceled'].value_counts())
# # plot.show()

# ----------------Reservation status in diff hotels(city and resort hotels) based on is_canceled------------
# plot.figure(figsize=(8, 4))
#
# # ===Problem 1== AttributeError: 'numpy.int64' object has no attribute 'startswith'
# # solution==The problem seems to be that the column I'm using for the hue is an integer and not a string
# df['is_canceled'] = df['is_canceled'].astype(str)
#
# plot.title("Reservation status in diff hotels")
# ax1 = sns.countplot(data=df, x='hotel', hue='is_canceled')
# #
# for bars in ax1.containers:
#     ax1.bar_label(bars)
# # plot.show()
# plot.xlabel('Hotel')
# plot.ylabel('No of reservations')
# plot.show()

# Above plot shows that how many cancellations happenning in both hotels
# City hotels reservation getting cancelled more

# check the percentage for above graph values

city_hotel = df[df['hotel'] == 'City Hotel']
print(city_hotel['is_canceled'].value_counts(normalize=True))
# city hotel reservations are 58 % but cancellation is 41 %

resort_hotel = df[df['hotel'] == 'Resort Hotel']  #it collects data of reort hotel only
print(resort_hotel['is_canceled'].value_counts(normalize=True))
# resort hotel reservations are 72 % but cancellation is only 27 %

# -----Find out why city hotels reservations getting cancelled? is it becz of high value
#finding avg daily rate for both hotels
#If a hotel has $50,000 in room revenue and 500 rooms sold, the ADR would be $100 ($50,000/500).
#we r taking mean value of one day average daily rate
resort_hotel =resort_hotel.groupby('reservation_status_date')[['adr']].mean()
# it will group by reservation status date and then we are taking mean values of ADR

city_hotel =city_hotel.groupby('reservation_status_date')[['adr']].mean()

# #--Create visualisation report for ADR
# plot.figure(figsize=(10,8))
# plot.title("Average Daily Rate in city and Resort Hotel")
# plot.plot(resort_hotel.index,resort_hotel['adr'],label=resort_hotel) #x=index is reservation status date
# plot.plot(city_hotel.index,city_hotel['adr'],label=city_hotel) #x=index is reservation status date
# #y=ADR
# plot.legend(fontsize=20)
# #plot.show()
#
# #Monthwise Visualisation of reservations
# df['is_canceled'] = df['is_canceled'].astype(str)
# df['month'] =df['reservation_status_date'].dt.month
# plot.figure(figsize=(10,5))
# ax=sns.countplot(x='month',hue='is_canceled',data=df)
# legend_labels,_=ax.get_legend_handles_labels()
# ax.legend(bbox_to_anchor=(1,1))
# plot.xlabel('month')
# plot.ylabel('number of reservations')
# plot.legend(['not canceled', 'canceled'])
# plot.show()

# Above graph shows that jan month is having most of the cacncellations and august has less

# plot.figure(figsize=(10,8))
# plot.title('ADR per month', fontsize=30)
# sns.barplot(x='month', y='adr', data=df[df['is_canceled'] == 1].groupby('month')[['adr']].sum().reset_index())
# plot.show()

cancelled_data=df[df['is_canceled']==1]
top_10_country =cancelled_data['country'].value_counts()[:10]
plot.figure(figsize=(8,8))
plot.title('Top 10 countries with reservation cancelled')
plot.pie(top_10_country,autopct='%.2f')
plot.show()

print(df['market_segment'].value_counts())
print(df['market_segment'].value_counts(normalize=True))

cancelled_df_adr=cancelled_data.groupby('reservation_status_date')[['adr']].mean()
cancelled_df_adr.reset_index(inplace=True)
cancelled_df_adr.sort_values('reservation_status_date',inplace=True)

not_cancelled_data=df[df['is_canceled']==0]
not_cancelled_data_df_adr= not_cancelled_data.groupby('reservation_status_date')[['adr']].mean()
not_cancelled_data_df_adr.reset_index(inplace=True)
not_cancelled_data_df_adr.sort_values('reservation_status_date',inplace=True)

plot.figure(figsize=(20,6))
plot.title('Average Daily Rate')
plot.plot(not_cancelled_data_df_adr['reservation_status_date'].not_canceled_df_adr['adr'],label="not canceled")
plot.plot(cancelled_df_adr['reservation_status_date'].canceled_df_adr['adr'],label="not canceled")
plot.legend()
plot.show()
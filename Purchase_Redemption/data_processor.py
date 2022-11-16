import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)
# 读数据
df_user_profile_table = pd.read_csv("./data/user_profile_table.csv")
df_user_balance_table = pd.read_csv("./data/user_balance_table.csv")
df_mfd_day_share_interest = pd.read_csv("./data/mfd_day_share_interest.csv")
df_mfd_bank_shibor = pd.read_csv("./data/mfd_bank_shibor.csv")
# 改时间字段
df_mfd_day_share_interest.rename(columns={'mfd_date': 'record_date'}, inplace=True)
df_mfd_bank_shibor.rename(columns={'mfd_date': 'record_date'}, inplace=True)
df_user_balance_table.rename(columns={'report_date': 'record_date'}, inplace=True)

df = df_user_balance_table.merge(df_user_profile_table, on='user_id')
print(df.columns)
gb = df.groupby('record_date', as_index=False).agg(men_cnt=('sex', lambda x: x[x == 1].count()),
                                                   women_cnt=('sex', lambda x: x[x == 0].count()),
                                                   user_cnt=('user_id', 'count'),
                                                   tBalance=('tBalance', 'sum'),
                                                   yBalance=('yBalance', 'sum'),
                                                   direct_purchase_amt=('direct_purchase_amt', 'sum'),
                                                   purchase_bal_amt=('purchase_bal_amt', 'sum'),
                                                   purchase_bank_amt=('purchase_bank_amt', 'sum'),
                                                   consume_amt=('consume_amt', 'sum'),
                                                   transfer_amt=('transfer_amt', 'sum'),
                                                   tftobal_amt=('tftobal_amt', 'sum'),
                                                   tftocard_amt=('tftocard_amt', 'sum'),
                                                   share_amt=('share_amt', 'sum'),
                                                   category1=('category1', 'sum'),
                                                   category2=('category2', 'sum'),
                                                   category3=('category3', 'sum'),
                                                   category4=('category4', 'sum'),
                                                   total_purchase_amt=('total_purchase_amt', 'sum'),
                                                   total_redeem_amt=('total_redeem_amt', 'sum'),
                                                   )
data = gb.merge(df_mfd_day_share_interest, on='record_date').merge(df_mfd_bank_shibor, on='record_date')

print(data.head())
data.to_csv('data.csv', index=False)

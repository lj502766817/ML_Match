import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import r_regression

pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)


def process_data():
    # 读数据
    df_user_profile_table = pd.read_csv("./data/user_profile_table.csv")
    df_user_balance_table = pd.read_csv("./data/user_balance_table.csv")
    df_mfd_day_share_interest = pd.read_csv("./data/mfd_day_share_interest.csv")
    df_mfd_bank_shibor = pd.read_csv("./data/mfd_bank_shibor.csv")
    # 改时间字段
    df_mfd_day_share_interest.rename(columns={'mfd_date': 'date'}, inplace=True)
    df_mfd_bank_shibor.rename(columns={'mfd_date': 'date'}, inplace=True)
    df_user_balance_table.rename(columns={'report_date': 'date'}, inplace=True)

    df = df_user_balance_table.merge(df_user_profile_table, on='user_id')
    gb = df.groupby('date', as_index=False).agg(men_cnt=('sex', lambda x: x[x == 1].count()),
                                                women_cnt=('sex', lambda x: x[x == 0].count()),
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
    purchase = gb.pop('total_purchase_amt')
    redeem = gb.pop('total_redeem_amt')
    data = gb.merge(df_mfd_day_share_interest, on='date').merge(df_mfd_bank_shibor, on='date')
    data.insert(data.shape[1], 'total_purchase_amt', purchase)
    data.insert(data.shape[1], 'total_redeem_amt', redeem)
    data['date'] = data['date'].astype('str')
    data['date'] = pd.to_datetime(data['date'])
    print(data.head())
    data.to_csv('./data/data.csv', index=False)


def show_data():
    data = pd.read_csv('./data/data.csv')
    date = data['date'].to_numpy().astype('str')
    purchase = data['total_purchase_amt'].to_numpy()
    redeem = data['total_redeem_amt'].to_numpy()

    plt.figure(figsize=(15, 5), layout='constrained')
    plt.plot(date, purchase, label='purchase')
    plt.plot(date, redeem, label='redeem')
    plt.xlabel('x label')
    plt.ylabel('y label')
    plt.title("data")
    plt.legend()
    plt.show()


def analise_feature():
    data = pd.read_csv('./data/data.csv')
    feature = data.columns[1:-2]
    x = data[feature]
    y1 = data['total_purchase_amt']
    y2 = data['total_redeem_amt']
    selector = VarianceThreshold(threshold=(.8 * (1 - .8)))
    selector.fit(x)
    feature_new = selector.get_feature_names_out(feature)
    # x_new = data[feature_new]
    # r1 = r_regression(x_new, y1)
    # r2 = r_regression(x_new, y2)
    # feature_new = feature_new[np.any([r1 > 0.2, r1 < -0.2, r2 > 0.2, r2 < -0.2], axis=0)]
    data_new = data[np.append(np.append(np.array(['date']), feature_new), ['total_purchase_amt', 'total_redeem_amt'])]
    data_new.to_csv('./data/data_new.csv', index=False)


analise_feature()

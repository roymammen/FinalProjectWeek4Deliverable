import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:Mcsi123$5@localhost:5432/lax_aqi_temp_db")
lax_temp_df = pd.read_sql("SELECT * FROM lax_aqi_temp_db;", engine)

def predict_week_mean_temp_ml(population,so2_conc,pm10_conc,pm2_5_conc,no2_conc,month_i,Week):
    #lax_temp_df = pd.read_csv("./lax_temp_aqi_ml_db.csv")

    # print(f'population:{population} so2_conc:{so2_conc} pm10_conc:{pm10_conc} pm2_5_conc:{pm2_5_conc} no2_conc:{no2_conc}, month_i:{month_i}')

    datetime_series = pd.to_datetime(lax_temp_df['date'], format="%m/%d/%Y")
    lax_temp_df['date'] = datetime_series
    # lax_temp_df
    # lax_temp_df.dtypes
    year0 = 2019
    year1 = 2018
    if ( month_i == 1 or month_i == 3 or month_i == 5 or month_i == 7 or month_i == 8 or month_i == 10 or month_i == 12):
        ds_y0 = f'2019-{month_i}-1'
        de_y0 = f'2019-{month_i}-31'
        ds_y1 = f'2018-{month_i}-1'
        de_y1 = f'2018-{month_i}-31'
    elif ( month_i == 2):
        ds_y0 = f'2019-{month_i}-1'
        de_y0 = f'2019-{month_i}-28'
        ds_y1 = f'2018-{month_i}-1'
        de_y1 = f'2018-{month_i}-28'
    else:
        ds_y0 = f'2019-{month_i}-1'
        de_y0 = f'2019-{month_i}-30'
        ds_y1 = f'2018-{month_i}-1'
        de_y1 = f'2018-{month_i}-30'

    # print(date_start)
    lax_temp_flt_mnth_ser = lax_temp_df.loc[(((lax_temp_df['date'] >= ds_y0) & (lax_temp_df['date'] <= de_y0)) | 
                                        ((lax_temp_df['date'] >= ds_y1) & (lax_temp_df['date'] <= de_y1))
                                       ),:].mean()
    # lax_temp_flt_mnth_ser
    lax_temp_flt_mnth_chng = [(0/100),(population/100),(0/100),(0/100),(so2_conc/100),(pm10_conc/100),(pm2_5_conc/100),(no2_conc/100),(month_i/100)]

    lax_temp_flt_mnth_chng = lax_temp_flt_mnth_chng * lax_temp_flt_mnth_ser
    lax_temp_flt_mnth_ser += lax_temp_flt_mnth_chng
    population = lax_temp_flt_mnth_ser[1]
    so2_conc   = lax_temp_flt_mnth_ser[4]
    pm10_conc  = lax_temp_flt_mnth_ser[5]
    pm2_5_conc = lax_temp_flt_mnth_ser[6]
    no2_conc   = lax_temp_flt_mnth_ser[7]
    # print(f'population:{population} so2_conc:{so2_conc} pm10_conc:{pm10_conc} pm2_5_conc:{pm2_5_conc} no2_conc:{no2_conc}')

    X = lax_temp_df[['population','lat','lon','so2_conc','pm10_conc','pm2_5_conc','no2_conc','month_day_ts']]
    y = lax_temp_df['avgtemp']

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=1)

    rf = RandomForestRegressor()
    rf.fit(X_train,y_train)
    print(f"Training Data Score: {rf.score(X_train, y_train)}")
    print(f"Testing Data Score: {rf.score(X_test, y_test)}")
    month_day_ts_comp = month_i+(Week/30)
    return rf.predict([[population,34.1365,-117.92391,so2_conc,pm10_conc,pm2_5_conc,no2_conc,month_day_ts_comp]])

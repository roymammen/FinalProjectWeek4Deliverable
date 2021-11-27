from flask import Flask, render_template, request
from run_ml import predict_week_mean_temp_ml

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/predict_wk_tmp',methods=['POST'])
def predict_wk_tmp():
    # Get the data from the POST request.
    if request.method == "POST":
        # print(request.form["Population"])
        population = int(request.form["population"])
        so2_conc = float(request.form["so2_conc"])
        pm10_conc = float(request.form["pm10_conc"])
        pm2_5_conc = float(request.form["pm2_5_conc"])
        no2_conc = float(request.form["no2_conc"])
        Month = int(request.form["Month"])
        Week = int(request.form["Week"])
        
        #month_day_ts = Month+(Week/30)
        month_i = Month
        #print("call my ml model predict_week_mean_temp_ml()")
        #print(f'app.py population:{population} so2_conc:{so2_conc} pm10_conc:{pm10_conc} pm2_5_conc:{pm2_5_conc} no2_conc:{no2_conc}, month_i:{month_i}')
        predict_week_mean_temp = predict_week_mean_temp_ml(population,so2_conc,pm10_conc,pm2_5_conc,no2_conc,month_i,Week) # call my ml model
        #print(predict_week_mean_temp)

        mean_temp = round(predict_week_mean_temp[0],2)
        #mean_temp=345.67
        print(f'mean_temp:{mean_temp}')

        results = f'Mean temperature for Month {Month} Week {Week} is {mean_temp} deg F'
        #print(results)
        
        return render_template("result.html", results=results)

from flask import Flask, render_template, request
import pickle
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)


classifier = pickle.load(open('price.pkl', 'rb'))


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


standard_to = StandardScaler()


@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        minimum_nights = int(request.form['nights'])
        availability_365 = int(request.form['days'])
        room_type = request.form['room']
        if room_type == 'private':
            room_type = 1
        elif room_type == 'shared':
            room_type = 2
        else:
            room_type = 0

        neighbourhood_group = request.form['area']
        if neighbourhood_group == 'Manhattan':
            neighbourhood_group = 0
        elif neighbourhood_group == 'Brooklyn':
            neighbourhood_group = 1
        elif neighbourhood_group == 'Queens':
            neighbourhood_group = 2
        elif neighbourhood_group == 'Bronx':
            neighbourhood_group = 3
        else:
            neighbourhood_group = 4

        number_of_reviews = request.form['reviews']
        if number_of_reviews == 'Low':
            number_of_reviews = 100
        elif number_of_reviews == 'Medium':
            number_of_reviews = 250
        else:
            number_of_reviews = 500

        reviews_per_month = request.form['month']
        if reviews_per_month == 'Low':
            reviews_per_month = float(5)
        elif reviews_per_month == 'Medium':
            reviews_per_month = float(15)
        else:
            reviews_per_month = float(27)

        prediction = classifier.predict([[neighbourhood_group, room_type, minimum_nights, number_of_reviews, reviews_per_month,
                                     availability_365]])
        output = prediction[0]
        if output > 0:
            return render_template('index.html', prediction_text="Price of the room is $"+format(round(output)))
        else:
            return render_template('index.html', prediction_text="Enter the details correctly to get the price")






if __name__ == "__main__":
    app.run(debug=True)

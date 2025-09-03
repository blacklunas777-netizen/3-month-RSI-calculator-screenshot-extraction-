import os
import cv2
import numpy as np
from flask import Flask, request, render_template, redirect, url_for
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    return img, edges

def extract_price_line(edges):
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    chart_contour = max(contours, key=cv2.contourArea)
    points = chart_contour.squeeze()
    points = points[np.argsort(points[:, 0])]
    return points

def map_pixels_to_prices(points, price_min, price_max, chart_height):
    prices = []
    for x, y in points:
        price = price_max - ((y / chart_height) * (price_max - price_min))
        prices.append(price)
    return savgol_filter(prices, 11, 3)

def calculate_rsi(prices, period=14):
    deltas = np.diff(prices)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    avg_gain = np.convolve(gains, np.ones(period)/period, mode='valid')
    avg_loss = np.convolve(losses, np.ones(period)/period, mode='valid')
    rs = avg_gain / (avg_loss + 1e-6)
    rsi = 100 - (100 / (1 + rs))
    return rsi

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        price_min = float(request.form['price_min'])
        price_max = float(request.form['price_max'])
        chart_height = int(request.form['chart_height'])

        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            _, edges = preprocess_image(filepath)
            points = extract_price_line(edges)
            prices = map_pixels_to_prices(points, price_min, price_max, chart_height)
            rsi = calculate_rsi(prices)

            # Plot RSI
            plt.figure(figsize=(10, 4))
            plt.plot(rsi, label='RSI')
            plt.axhline(70, color='red', linestyle='--', label='Overbought')
            plt.axhline(30, color='green', linestyle='--', label='Oversold')
            plt.title('RSI Indicator')
            plt.xlabel('Time')
            plt.ylabel('RSI')
            plt.legend()
            plt.grid(True)
            plot_path = os.path.join(app.config['UPLOAD_FOLDER'], 'rsi_plot.png')
            plt.savefig(plot_path)
            plt.close()

            return render_template('result.html', image=filename, plot='rsi_plot.png')

    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port, debug=True)

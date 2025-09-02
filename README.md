# RSI Microservice 📈

A lightweight Flask-based microservice that extracts price data from Robinhood-style chart screenshots and calculates the RSI (Relative Strength Index) indicator.

## 🔧 Features

- Upload chart screenshots (e.g., 3-month crypto charts)
- Visual extraction of price line using OpenCV
- RSI calculation from pixel-mapped price data
- Interactive preview of uploaded chart and RSI plot
- Ready for public deployment on Render

## 🚀 Deployment (Render)

1. Push this repo to GitHub
2. Go to [https://render.com](https://render.com)
3. Create a new **Web Service** → Connect your GitHub repo
4. Use these settings:

| Setting           | Value                          |
|-------------------|--------------------------------|
| Environment       | Python                         |
| Build Command     | `pip install -r requirements.txt` |
| Start Command     | `python app.py`                |
| Instance Type     | Free                           |

## 🧪 Local Development

```bash
pip install -r requirements.txt
python app.py

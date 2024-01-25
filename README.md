![ppplogo](/static/images/ppp.png)
#
<p align="center">
    A Flask application that displays current NBA player score predictions. Please take a look below.
</p>
<div align="center">
  <img src="https://img.shields.io/badge/maintenance-experimental-blue.svg" alt="Maintained status" />
  <img src="https://img.shields.io/github/v/release/KevinTrinh1227/Prize-Pick-Predictions.svg" alt="Release badge" />
</div>

![3b3f8646e52a86ce072b400c358e9a22](https://user-images.githubusercontent.com/48145892/234551198-3f3d0d0a-fd37-486f-836c-31a0f97fc26e.gif)

## 📌 Important Information
This project was made as just a concept. Due to many project constraints, and technical barriers during the project's initial stages, I have decided not to develop this project and it has since been archived. Currently, the application only draws predictions using player averages and compares them to the betting strike prices. While this does work, it nowhere near approaches the precision and complexity of using Multiple Linear, Ridge, or even Polynomial regression predictions.

While this project is no longer in an archive, I will slowly commit and integrate appropriate machine-learning algorithms to generate more accurate predictions using the correlation between different combinations of points, rebounds, and assists with the opponent team's ELO, and potentially other variables down the way including home court advantage, fouls, injuries, etc. 

## 🏀 What is Prize Pick Predictions?
This Python project is a Flask application that provides "recommendations" for sports betting. With a focus on accuracy and data-driven insights, the app delivers relevant and timely information through multiple APIs, ensuring users can access up-to-date data and statistics. Designed to offer valuable insights and recommendations, this app caters to experienced and novice sports bettors, providing an edge in the competitive world of sports betting.

##  🛠 Getting Started

### Clone the Repository
1) Open the desired directory in the command prompt
2) Clone the repository using the command below

    ```sh
    git clone https://github.com/KevinTrinh1227/Prize-Pick-Predications.git
    ```

### Initial set-up process

1. Install dependencies

   ```sh
   pip install -r requirements.txt
   ```
2. Install [Firefox](https://www.mozilla.org/en-US/firefox/new/) & [Gecko Driver](https://github.com/mozilla/geckodriver/releases)
   
   ```sh
   # Windows driver creation
   firefox_options = Options()
   firefox_options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'  # Firefox binary location
   driver = webdriver.Firefox(service=service, options=firefox_options)
   ```
   ```sh
   # Linux Ubuntu driver creation
   driver = webdriver.Firefox()
   ```
## 🚀 Host the app locally

1. Run the app and get the HTTP link

   ```sh
   python main.py
   ```
2. Open the `http://127.0.0.1:5000` link on a web browser

   ```sh
   ~\Prize-Pick-Predications>app.py
    * Serving Flask app 'app'
    * Debug mode: off
    * Running on http://127.0.0.1:5000
   ```
   

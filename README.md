![ppplogo](/static/images/ppp.png)
#
This Python project is a Flask application that utilizes linear regression, a powerful machine learning algorithm, to provide recommendations for sports betting. With a focus on accuracy and data-driven insights, the app delivers relevant and timely information through multiple APIs, ensuring users have access to up-to-date data and statistics. Designed to offer valuable insights and recommendations, this app caters to both experienced and novice sports bettors, providing an edge in the competitive world of sports betting.

# At a Glance
![3b3f8646e52a86ce072b400c358e9a22](https://user-images.githubusercontent.com/48145892/234209657-1bd8dcce-7cbc-40da-808c-8f60f34fb551.gif)

Advanced Topics: Programming for Data Science <strong>CS 4375</strong> Project. Still under development. 

## Getting Started

### 📋 Clone the Repository
1) Open desired directory in command prompt
2) Clone the repository using the command below

    ```sh
    git clone https://github.com/KevinTrinh1227/Prize-Pick-Predications.git
    ```

### 🛠 set-up
1. Use link below or [click here](https://api.prizepicks.com/projections?league_id=7) then copy everything to clipboard

   ```sh
   https://api.prizepicks.com/projections?league_id=7)
   ```

2. Paste everything into the json file below (because prize picks no longer supports public api)
   ```sh
   json files/pre_formatted.json
   ```

3. Install dependencies

   ```sh
   pip install scikit-learn
   ```
   ```sh
   pip install flask
   ```
   ```sh
   pip install requests
   ```
   ```sh
   pip install tabulate
   ```
### 🚀 Execute the app in terminal

1. Run the main file and wait untill 100% of players has been processed

   ```sh
   python main.py
   ```
2. Deploy the Flask app and view recommendations

   ```sh
   python app.py
   ```

# Dashboard with real-time information about Warsaw real estate market

Data flow:
1. Every hour a scraper set up on Raspberry Pi is gathering flat selling ads
2. Data is aggregated and statistics regarding each district and/or flat size is hosted as a [JSON file](https://raw.githubusercontent.com/mbalcerzak/warsaw_flats_api/main/json_dir/flats.json)
3. New aggregated data for the dashboard is generated every day at 00:40 CEST
4. Dashboard was built usind Dash (Python3.9) and is hosted on Heroku [Link to the App](https://warsaw-flats.herokuapp.com/)

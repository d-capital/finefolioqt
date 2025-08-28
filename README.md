# FineFolio Desktop
This app is build to update economic information on 7 major economies to make regression analysis (Random Forest Regression)
to see if current exchange rate is overvalued or underestimated. Its based on interest rate, inflation, unemployment, gdp and trade balance.
All factors are presented in annual format. 
Every 15 minutes app goes into investing.com and downloads latest events for thoses factors for 7 major economies.
App allows you to download series of events as csv, see side by side comparison of economies based on currency pairs.

### Building on your own
Clone the repository, setup virtual environment, install dependencies from requirements.txt, then build the app
`pyinstaller --onefile --noconsole --icon=icon.ico --name FineFolio main.py`
Results will be saved into `dist` folder.
Copy `finefolio.db` into `dist` folder.
Run `FineFolio.exe`.

### Downloading prebuild version
Download `finefolio.zip`, unpack it, it already has `finefolio.db`.
Run `FineFolio.exe`.

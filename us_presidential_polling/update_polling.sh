python3 ~/code/us_presidential_polling/trump_polling.py

cwd=$(pwd)

cd ~/code

git add .
git commit -m "Hourly Data Update."
git push origin main

cd "$cwd"


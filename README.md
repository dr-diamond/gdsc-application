# GDSC application

This is my application for SNU's GDSC club. 
For styling the page, I decided to switch from tailwind to plain CSS. I find the seperate stylesheets easier to read, and easier to apply the same properties to multiple elements at the same time.  

I opted for Flask in the backend due to my comfort with python, and it's lightweightedness and relatively simpler syntax over other python web frameworks like Django.  

I decided to have both account creation and comment functionality in the website. Due to the time crunch, I didn't have time to add more user functionality or style the website better.  

The app is deployed [here](https://gdsc-application-39f80c1wc-dr-diamonds-projects.vercel.app/), but due to issues with Vercel's storage, account creation and comment functionality works only when run locally. The app can be run locally simply by creating an APP_SECRET_KEY env variable and running app.py.

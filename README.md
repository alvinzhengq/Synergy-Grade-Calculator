# Synergy-Grade-Calculator
A Localhost Server Client Based Application for retrieving grades from Synergy and letting you to test out what new assignments will do to your grade.

Release page: https://github.com/alvinzhengq/Synergy-Grade-Calculator/releases

## Why a Localhost Browser App?
So you might be asking why a localhost broswer app instead of a windowed application. This is because of 2 reasons.

First, this project uses the python version of Selenium to retrieve data. Python has some decent window application libraries, but they aren't as good as C++, and C++ doesn't have good support for Selenium. In addition, I had recently been working a lot with Flask, and so I made the decision to create the app using Flask and Selenium in Python.

Secondly, JS libraries such as Vue.js has made web apps much more sophiscated and are much more advanced. So using a web application has opened up a variety of options for doing things, much more than the traditional windowed application. Additionally, by splitting up the application into the front end powered by Vue.js and the backend powered by Flask, I was able to organize my work much more effectively with the backend focused on getting data, while the frontend focused on presenting that data.

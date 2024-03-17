#!/bin/bash
export FLASK_ENV=development
export FLASK_DEBUG=0
export WOLFIT_SETTINGS=$(pwd)/dev.settings
export MONGO_URI=mongodb+srv://iromanmartinez19:UFpeNT0FEDAC5IJ4@hw04@hw04.vtusxbg.mongodb.net/?retryWrites=true&w=majority&appName=HW0

flask run --host=0.0.0.0 --port=8080

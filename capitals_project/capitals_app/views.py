
from django.shortcuts import render
import requests
import random


def home(request):
    try:
        # Send an HTTP GET request to the API endpoint that retrieves all countries and their capitals
        response = requests.get(
            'https://countriesnow.space/api/v0.1/countries/capital')

        # Extract the data (a list of countries and their capitals) from the API response
        data = response.json()['data']

        # Select a random country-capital pair from the data list
        random_country_capital = random.choice(data)

        # Store the correct capital in the session
        request.session['correct_capital'] = random_country_capital['capital']

        # Render the home.html template with the random country-capital pair
        return render(request, 'home.html', {'country': random_country_capital['name']})

    except requests.exceptions.RequestException as e:
        # Handle the exception (e.g. log the error, show a friendly error message to the user, etc.)
        error_message = f"An error occurred while retrieving data from the API: {e}"
        return render(request, 'error.html', {'error_message': error_message})


def check_guess(request):
    guess = request.POST.get('guess')
    correct_capital = request.session.get('correct_capital')
    country = request.POST.get('country')

    # Check if the guess is correct
    if guess == correct_capital:
        message = "Correct!"
    else:
        message = f"Incorrect. The correct capital of {country} is {correct_capital}."

    # Clear the session
    request.session.flush()

    # Render the result template with the message
    return render(request, 'result.html', {'message': message})

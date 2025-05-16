# wordgame/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from django.templatetags.static import static # Сүрөттөрдүн URL'ин алуу үчүн
import random

# Оюн үчүн сөздөр жана сүрөттөр
# Сүрөттөр static/wordgame/images/ папкасында жайгашышы керек
WORDS_DATA = [
    {'word': "алма", 'image_path': "wordgame/images/apple.png"}, # .png же .jpg
    {'word': "китеп", 'image_path': "wordgame/images/book.png"},
    {'word': "күн", 'image_path': "wordgame/images/sun.png"},
    {'word': "мышык", 'image_path': "wordgame/images/cat.png"},
    {'word': "топ", 'image_path': "wordgame/images/ball.png"},
    # Бул жерге өзүңүздүн сөздөрүңүздү жана сүрөттөрүңүздүн жолдорун кошуңуз
    # Мисал үчүн бир нече сүрөттүн атын жаздым, сизде бул сүрөттөр болушу керек
]

MAX_INCORRECT_GUESSES = 6 # Бул сан торчонун уячаларынын санына барабар же андан аз болушу керек
                          # Мисалы, 6 ката болсо, 2x3 торчо жетиштүү

def initialize_game(request):
    selected_data = random.choice(WORDS_DATA)
    word_to_guess = selected_data['word'].lower()
    image_url = static(selected_data['image_path']) # Сүрөттүн толук URL'ин алуу

    request.session['word_to_guess'] = word_to_guess
    request.session['image_url'] = image_url # Сүрөттүн URL'ин сессияга сактоо
    request.session['guessed_letters'] = []
    request.session['incorrect_guesses_left'] = MAX_INCORRECT_GUESSES
    request.session['game_over'] = False
    request.session['game_won'] = False
    request.session['message'] = "Оюн башталды! Бир тамга киргизиңиз."
    request.session['used_letters'] = []
    # Торчонун абалын сактоо үчүн (кайсы уячалар ачык)
    request.session['grid_cells_revealed'] = [False] * MAX_INCORRECT_GUESSES # Башында баары жабык

def display_word(word, guessed_letters):
    displayed = ""
    for letter in word:
        if letter in guessed_letters:
            displayed += letter + " "
        else:
            displayed += "_ "
    return displayed.strip()

def hangman_view(request):
    if 'word_to_guess' not in request.session or request.session.get('game_over', False):
        initialize_game(request)

    word_to_guess = request.session['word_to_guess']
    image_url = request.session['image_url'] # Сүрөттүн URL'ин алуу
    guessed_letters = request.session.get('guessed_letters', [])
    incorrect_guesses_left = request.session.get('incorrect_guesses_left', MAX_INCORRECT_GUESSES)
    game_over = request.session.get('game_over', False)
    game_won = request.session.get('game_won', False)
    message = request.session.get('message', '')
    used_letters = request.session.get('used_letters', [])
    grid_cells_revealed = request.session.get('grid_cells_revealed', [False] * MAX_INCORRECT_GUESSES)


    if request.method == 'POST' and not game_over:
        guess = request.POST.get('letter', '').lower()

        if len(guess) == 1 and guess.isalpha():
            if guess in used_letters:
                message = f"'{guess}' тамгасы мурда колдонулган. Башка тамга киргизиңиз."
            else:
                used_letters.append(guess)
                request.session['used_letters'] = used_letters

                if guess in word_to_guess:
                    guessed_letters.append(guess)
                    request.session['guessed_letters'] = guessed_letters
                    message = f"Туура! '{guess}' тамгасы сөздө бар."
                    if all(letter in guessed_letters for letter in word_to_guess):
                        game_won = True
                        game_over = True
                        message = f"Куттуктайм! Сиз '{word_to_guess.upper()}' сөзүн таптыңыз! Бул '{word_to_guess.upper()}' эле."
                        # Утканда бардык уячаларды ачуу
                        grid_cells_revealed = [True] * MAX_INCORRECT_GUESSES
                        request.session['grid_cells_revealed'] = grid_cells_revealed
                else:
                    incorrect_guesses_left -= 1
                    request.session['incorrect_guesses_left'] = incorrect_guesses_left
                    
                    # Торчонун бир уячасын ачуу
                    incorrect_guesses_count = MAX_INCORRECT_GUESSES - incorrect_guesses_left -1
                    if incorrect_guesses_count < MAX_INCORRECT_GUESSES and not grid_cells_revealed[incorrect_guesses_count]:
                        grid_cells_revealed[incorrect_guesses_count] = True
                    request.session['grid_cells_revealed'] = grid_cells_revealed
                    
                    message = f"Ката! '{guess}' тамгасы сөздө жок. {incorrect_guesses_left} аракет калды."
                    if incorrect_guesses_left <= 0:
                        game_over = True
                        message = f"Тилекке каршы, утулуп калдыңыз! Жашыруун сөз: '{word_to_guess.upper()}'"
                        # Утулганда да бардык уячаларды ачуу
                        grid_cells_revealed = [True] * MAX_INCORRECT_GUESSES
                        request.session['grid_cells_revealed'] = grid_cells_revealed
                        
        elif len(guess) != 1 :
             message = "Сураныч, бир гана тамга киргизиңиз."
        else:
            message = "Сураныч, тамга киргизиңиз."
        
        request.session['game_over'] = game_over
        request.session['game_won'] = game_won
        request.session['message'] = message

    displayed_word_str = display_word(word_to_guess, guessed_letters)
    
    context = {
        'displayed_word': displayed_word_str,
        'guesses_left': incorrect_guesses_left,
        'used_letters_list': sorted(list(set(used_letters))),
        'message': message,
        'game_over': game_over,
        'game_won': game_won,
        'alphabet': "абвгдеёжзийклмнңоөпрсстууүфхцчшщъыьэюя",
        'image_to_guess_url': image_url, # Сүрөттүн URL'ин шаблонго жөнөтүү
        'grid_cells_revealed': grid_cells_revealed, # Торчонун абалын жөнөтүү
        'grid_total_cells': MAX_INCORRECT_GUESSES # Торчодо канча уяча болорун жөнөтүү (мис., 2x3)
    }
    return render(request, 'wordgame/hangman_template.html', context)

def new_hangman_game_view(request):
    initialize_game(request)
    return redirect(reverse('hangman_play'))
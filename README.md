
# 🕹️ Django "Hangman" Game

A classic **Hangman** game built with Django. Guess the hidden word one letter at a time before you run out of attempts!

---

## 🎯 Purpose

To showcase Django essentials:

* Views, Templates, URLs, Forms
* Game state stored in **sessions**
* String handling, conditions, loops
* Basic frontend logic with HTML/CSS/JS

---

## 🛠️ Tech Stack

* Python 3 🐍
* Django 5.x 🌐
* HTML + CSS

---

## ⚙️ How to Run

```bash
git clone [YOUR_REPO_URL]
cd django_hangman_game

python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Visit 👉 `http://127.0.0.1:8000/hangman/play/`

---

## 🧩 Game Logic

* Random word chosen from a list
* User guesses letters one by one
* Correct guesses are revealed in place
* Wrong guesses reduce attempts and draw the hangman (via JS/CSS)
* Game ends on win or loss
* Previously guessed letters and remaining attempts are shown

---

## 📁 Key Components

* `views.py` — game & restart logic
* `urls.py` — routing
* `hangman_template.html` — UI + logic
* `settings.py` — project config
* Sessions — to track word, guesses, and attempts
![IMAGE 2025-05-16 11:53:58](https://github.com/user-attachments/assets/55ead3ac-dbbf-43e2-9b73-75301e3aa226)
![IMAGE 2025-05-16 11:54:13](https://github.com/user-attachments/assets/b5cedfb7-7e67-4008-804f-8ee5f9a30c52)





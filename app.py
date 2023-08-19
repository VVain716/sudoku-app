import numpy as np
from ctypes import CDLL, c_int, POINTER
from flask import Flask, render_template, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
import random
from cs50 import SQL
from helpers import login_required, apology
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///grids.db")
solver = CDLL('./solve.so')

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

solver.execute.restype = POINTER(POINTER(c_int))


@app.route('/', methods = ["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        inputStr = request.form.get('inputStr')
        with open('board.txt', 'w') as file:
            for i in range(1, 10):
                file.write(inputStr[(9 * (i - 1)):(9 * i)])
                file.write('\n')
        board = solve_board()
        retStr = ""
        for i in range(9):
            for j in range(9):
                retStr += str(board[i][j])
        return render_template('index.html', retStr=retStr, boldStr=inputStr)
    else:
        return render_template('index.html', retStr="")

@app.route('/easy')
@login_required
def easy():
    file = open('board.txt', 'w')
    retStr = rand_sudoku('easy')
    for i in range(9):
        for j in range(9):
            file.write(retStr[9 * i + j])
        file.write('\n')
    file.close()
    board = solve_board()
    solveStr = ""
    for i in range(9):
        for j in range(9):
            solveStr += str(board[i][j])
    return render_template('easy.html', retStr=retStr, solveStr=solveStr, boldStr=retStr)
@app.route('/medium')
@login_required
def medium():
    file = open('board.txt', 'w')
    retStr = rand_sudoku('medium')
    for i in range(9):
        for j in range(9):
            file.write(retStr[9 * i + j])
        file.write('\n')
    file.close()
    board = solve_board()
    solveStr = ""
    for i in range(9):
        for j in range(9):
            solveStr += str(board[i][j])
    return render_template('medium.html', retStr=retStr, solveStr=solveStr, boldStr=retStr)
@app.route('/hard')
@login_required
def hard():
    file = open('board.txt', 'w')
    retStr = rand_sudoku('hard')
    for i in range(9):
        for j in range(9):
            file.write(retStr[9 * i + j])
        file.write('\n')
    file.close()
    board = solve_board()
    solveStr = ""
    for i in range(9):
        for j in range(9):
            solveStr += str(board[i][j])
    return render_template('hard.html', retStr=retStr, solveStr=solveStr, boldStr=retStr)
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("Not username entered")
        elif not request.form.get("password"):
            return apology("No password")
        elif not request.form.get("conformation"):
            return apology("Enter conformation")
        
        users = db.execute("SELECT username FROM users WHERE username = ?", request.form.get("username"))
        if len(users) != 0:
            return apology("user already exists")
        password = request.form.get("password")
        conformation = request.form.get("conformation")
        if password != conformation:
            return apology("Passwords do not match")
        username = request.form.get("username")
        password_hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, password_hash)
        return redirect("/")
    else:
        return render_template("register.html")
    
def rand_sudoku(difficulty):
    if difficulty not in ['easy', 'medium', 'hard']:
        raise ValueError
    with open(f"examples/{difficulty}.txt") as file:
        rows = file.readlines()
        return rows[random.randint(0, len(rows))]

def solve_board():
    board_ptr = solver.execute()

    board_size = 9
    board = np.zeros((board_size, board_size), dtype=np.int32)    

    for i in range(board_size):
        for j in range(board_size):
            board[i, j] = board_ptr[i][j]
    solver.free_board(board_ptr, board_size)
    return board
    
app.run()

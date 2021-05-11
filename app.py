from flask import Flask, render_template, redirect, url_for, request, flash
import json

app = Flask(__name__)
app.secret_key = b'5c|dQ`H\CaE&<75zk4"{S'

with open('flag.json') as f:
    flags = json.load(f)

with open('message.json') as f:
    message = json.load(f)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/flag', methods=['POST'])
def flag():
    problem = request.form.get('problem')
    to_check_flag = request.form.get('flag')
    if not problem or not to_check_flag or problem not in {'pA', 'pB', 'pC', 'pD', 'pE', 'pF'}:
        flash('Something went wrong!', 'warning')
        return redirect(url_for('index'))
    easy = flags[problem]['easy'] == to_check_flag
    hard = flags[problem]['hard'] == to_check_flag
    if not easy and not hard:
        flash('Something went wrong!', 'warning')
    elif easy:
        flash(f"Easy mission completed: {message[problem]['easy']}", 'success')
    elif hard:
        flash(f"Hard mission completed: {message[problem]['hard']}", 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()

from flask import Flask, render_template, redirect, url_for, request, flash, make_response
import json
import time

app = Flask(__name__)
app.secret_key = b'5c|dQ`HCaE&<75zk4"{S'

with open('flag.json') as fp:
    flags = json.load(fp)

with open('message.json') as fp:
    message = json.load(fp)


@app.route('/')
def index():
    if not request.cookies.get('completed'):
        resp = make_response(render_template('index.html', completed=None))
        resp.set_cookie(key='completed', value=json.dumps({}), expires=time.time() + 6 * 60)
        return resp
    else:
        completed = sorted(json.loads(request.cookies.get('completed')))
        return render_template('index.html', completed=completed)


@app.route('/flag', methods=['POST'])
def flag():
    problem = request.form.get('problem')
    to_check_flag = request.form.get('flag')
    if not problem or not to_check_flag or problem not in {'pA', 'pB', 'pC', 'pD', 'pE', 'pF'}:
        flash('Something went wrong!', 'warning')
        return redirect(url_for('index'))
    easy = flags[problem]['easy'] == to_check_flag
    hard = flags[problem]['hard'] == to_check_flag
    resp = make_response(redirect(url_for('index')))
    completed = json.loads(request.cookies.get('completed'))
    if not easy and not hard:
        flash('Something went wrong!', 'warning')
    elif easy:
        flash(f"Easy mission completed: {message[problem]['easy']}", 'success')
        completed[problem + 'easy'] = True
    elif hard:
        flash(f"Hard mission completed: {message[problem]['hard']}", 'success')
        completed[problem + 'hard'] = True
    if easy or hard:
        resp.set_cookie(key='completed', value=json.dumps(completed), expires=time.time() + 6 * 60)
        with open('record.json', 'w') as f:
            json.dump(completed, f)
    return resp


@app.route('/problem/<problem_id>')
def get_problem(problem_id):
    if problem_id not in {'pA', 'pB', 'pC', 'pD', 'pE', 'pF'}:
        return render_template('index.html'), 404
    else:
        return render_template('problems/' + problem_id + '.html')


@app.route('/record')
def record():
    with open('record.json') as f:
        completed = json.load(f)
    return render_template('record.html', completed=completed)


@app.route('/reset')
def reset():
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie(key='completed', expires=0)
    with open('record.json', 'w') as f:
        json.dump({}, f)
    return resp


if __name__ == '__main__':
    app.run()

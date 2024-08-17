from flask import Flask, render_template, redirect, request, flash
from surveys import satisfaction_survey # imports survey. 

print(satisfaction_survey)  # check if import works


app = Flask(__name__)

# Set secret key for session management and flash messages. 
app.secret_key = "my_secret_key"

responses = []

# route for start page of survey. 
@app.route('/')
def start():
    # render start.html; and pass thr survey object to the template
    return render_template('start.html', survey=satisfaction_survey)

@app.route('/questions/<int:qid>')
def show_question(qid):
    # if user tries to access invalid question, flash message and redirect them to next question.
    if len(responses) != qid:
        flash("You're trying to access an invalid question.")
        return redirect(f'/questions/{len(responses)}')
    # get curreent question based on question id, and render the question.
    question = satisfaction_survey.questions[qid]
    return render_template('question.html', question=question, qid=qid)


# handle answers
@app.route('/answer', methods=["POST"])
def handle_answer():
    # retrieve the anserr submitted via form, and append it to the responses list. 
    answer = request.form['answer']
    responses.append(answer)

    # increment qid to move to next question.
    qid = int(request.form['qid']) + 1

    # if user answers all questions redirect them to the thank you page. 
    if qid >= len(satisfaction_survey.questions):
        return redirect('/thankyou')
    else:
        # if there are more questions left, redirect to next question.
        return redirect(f'/questions/{qid}')



# added route for thank you page, 
@app.route('/thankyou')
def thank_user():
    return render_template('thankyou.html')



if __name__ == "__main__":
    app.run(debug=True)


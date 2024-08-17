from flask import Flask, render_template, redirect, request, flash, session
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

#############################################################################
# NEW ROUTE TO HANDLE POST REQUEST THAT INITIALIZES session['responses']
@app.route('/start-survey', methods=["POST"])
def start_survey():
    session["responses"] = [] # initalized empty lists to hold responsess in
    return redirect('/questions/0') #redirect to 1st question

@app.route('/questions/<int:qid>')
def show_question(qid):
    # get responses from the current session
    responses = session.get("responses", [])

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
    # Get responses from the session
    responses = session.get("responses", [])

    # Retrieve the answer submitted via the form
    answer = request.form['answer']
    # Retrieve the comment if the form has it
    comment = request.form.get('comment', None)

    # Add both the answer and the comment to the responses list
    responses.append({"answer": answer, "comment": comment})

    # Save the updated responses back to the session
    session["responses"] = responses

    # Determine the next question ID
    qid = len(responses)

    # If all questions are answered, redirect to the thank-you page
    if qid >= len(satisfaction_survey.questions):
        return redirect('/thankyou')
    else:
        return redirect(f'/questions/{qid}')




# added route for thank you page, 
@app.route('/thankyou')
def thank_user():
    return render_template('thankyou.html')


@app.route('/debug-session')
def debug_session():
    # Display the session data on the page
    return f"Session data: {session.get('responses', [])}"



if __name__ == "__main__":
    app.run(debug=True)


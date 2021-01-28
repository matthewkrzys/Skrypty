import sqlite3

conn = sqlite3.connect('rules.sqlite')


def db_setup():
    conn.execute("CREATE VIRTUAL TABLE rules USING fts5(question,answer);")
    cur = conn.cursor()

    cur.execute(
        'INSERT INTO rules(question,answer) VALUES("The app if freezing after I click run button","You need to clean up the cache. Please go to ...");')
    cur.execute(
        'INSERT INTO rules(question,answer) VALUES("I don t know how to proceed with the invoice","Please go to Setting, next Subscriptions and there is the Billing section");')
    cur.execute(
        'INSERT INTO rules(question,answer) VALUES("I get an error when I try to install the app","Could you plese send the log files placed in ... to ...");')
    cur.execute(
        'INSERT INTO rules(question,answer) VALUES("It crash after I have updated it","Please restart your PC");')
    cur.execute(
        'INSERT INTO rules(question,answer) VALUES("I cannot login in to the app","Use the forgot password button to setup a new password");')
    cur.execute(
        'INSERT INTO rules(question,answer) VALUES("I m not able to download it","Probably you have an ad blocker plugin installed and it blocks the popup with the download link");')

    conn.commit()


db_setup()


welcome = "Hi! I'm Arthur, the customer support chatbot. How can I help you?"

questions = (
    "The app if freezing after I click run button",
    "I don't know how to proceed with the invoice",
    "I get an error when I try to install the app",
    "It crash after I have updated it",
    "I cannot login in to the app",
    "I'm not able to download it"
            )

answers = (
        "You need to clean up the cache. Please go to ...",
        "Please go to Setting, next Subscriptions and there is the Billing section",
        "Could you plese send the log files placed in ... to ...",
        "Please restart your PC",
        "Use the forgot password button to setup a new password",
        "Probably you have an ad blocker plugin installed and it blocks the popup with the download link"
            )

def bm25(question):
    cur = conn.cursor()
    query = cur.execute("SELECT answer, bm25(rules) FROM rules WHERE rules MATCH 'question: "+str(question)+"' ORDER BY bm25(rules) LIMIT 0,1;")
    return cur.fetchall()

def get_highest_similarity(customer_question):
    return bm25(customer_question)


def run_chatbot():
    print(welcome)
    question = ""
    while question != "thank you":
        question = input()
        answer = get_highest_similarity(question)
        print(answer)


run_chatbot()
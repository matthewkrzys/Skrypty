import jellyfish

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

similarity_treshold = 0.2


def levenstein_distance(sentence1, sentence2):
    distance = jellyfish.levenshtein_distance(sentence1, sentence2)
    normalized_distance = distance / max(len(sentence1), len(sentence2))
    return 1.0 - normalized_distance


def get_highest_similarity(customer_question):
    max_distance = 0
    for question_id in range(len(questions)):
        distance = levenstein_distance(customer_question, questions[question_id])

        if distance > max_distance:
            highest_index = question_id
            max_distance = distance
    if max_distance > similarity_treshold:
        return answers[highest_index]
    else:
        return "The issues has been saved. We will contact you soon."


def run_chatbot():
    print(welcome)
    question = ""
    while question != "thank you":
        question = input()
        answer = get_highest_similarity(question)
        print(answer)


run_chatbot()

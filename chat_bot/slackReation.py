from flask import Flask, request
from slackeventsapi import SlackEventAdapter
import os

app = Flask(__name__)

SLACK_SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']

slack_events_adapter = SlackEventAdapter(
    SLACK_SIGNING_SECRET, "/slack/events", app
)

@slack_events_adapter.on("reaction_added")
def reaction_added(event):
 print("Hello")
 emoji = event.get("event").get("reaction")
 print(emoji)

@app.route("/slack/events",methods=['GET','POST'])
def authorize():
  output = request.get_json()
  print(output)
  return output["challenge"]

if __name__ == "__main__":
  app.run(port=3000)
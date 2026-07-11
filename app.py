import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from pangea_ai.matching import find_match
from pangea_ai.profiles import RESEARCHERS

load_dotenv()

app = App(token=os.environ["SLACK_BOT_TOKEN"])

@app.message()
def handle_message(message, say):
    text = message.get("text", "")
    
    # Ignore slash commands caught as messages
    if text.startswith("/"):
        return
    
    print(f"📨 Message received: {text}")
    result = find_match(text)
    
    if result:
        say(blocks=result, text="Pangea AI found a research match!")

@app.command("/pangea")
def handle_pangea_command(ack, command, say):
    ack()
    text = command.get("text", "").strip()
    print(f"🔬 Slash command: {text}")
    
    if not text:
        say(
            blocks=[
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "🌍 Welcome to Pangea AI"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Pangea AI bridges global vaccine research by connecting scientists with complementary expertise and unique field access.*\n\nTry a research topic to find your ideal collaborator:"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "• `/pangea oropouche virus transmission`\n• `/pangea Lassa fever hemorrhagic`\n• `/pangea chikungunya modeling`\n• `/pangea seroprevalence field data`"
                    }
                }
            ],
            text="Welcome to Pangea AI!"
        )
        return
    
    say("🔍 _Pangea AI is analyzing your research topic..._")
    result = find_match(text)
    
    if result:
        say(blocks=result, text="Pangea AI found a research match!")
    else:
        say(
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "🌍 *Pangea AI* — No match found for this topic.\nTry: `oropouche`, `Lassa fever`, `chikungunya`, `hemorrhagic fever`, `seroprevalence`"
                    }
                }
            ],
            text="No match found."
        )

@app.action("draft_intro_message")
def handle_draft_message(ack, body, say, client):
    ack()
    
    value = body["actions"][0]["value"]
    researcher_a_key, researcher_b_key = value.split("|")
    
    a = RESEARCHERS[researcher_a_key]
    b = RESEARCHERS[researcher_b_key]
    
    say("✍️ _Pangea AI is drafting your personalized introduction message..._")
    
    from anthropic import Anthropic
    ai_client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    
    # Determine seniority dynamic
    exp_gap = abs(a['years_experience'] - b['years_experience'])
    if exp_gap > 8:
        dynamic = f"{a['name']} is a senior researcher reaching out to mentor {b['name']}"
    else:
        dynamic = f"Two peers with complementary expertise connecting for collaboration"

    prompt = f"""You are a world-class scientific relationship builder with exceptional soft skills.
Write a short, personalized introduction email from {a['name']} to {b['name']}.

Context:
- {dynamic}
- Sender: {a['name']}, {a['location']}, {a['years_experience']} years experience
  Expertise: {', '.join(a['subjects'][:3])}
  Methods: {', '.join(a['methods'][:2])}
- Recipient: {b['name']}, {b['location']}, {b['years_experience']} years experience
  Expertise: {', '.join(b['subjects'][:3])}
  Methods: {', '.join(b['methods'][:2])}

Rules:
1. Open with a warm, culturally appropriate greeting (adapt tone to {b['location']} academic culture)
2. Mention ONE specific paper or finding from the recipient's field that genuinely impressed the sender (invent a plausible real-sounding paper title and finding)
3. Explain in 1-2 sentences exactly why their expertise is complementary — be scientifically specific
4. Propose a concrete next step (15-min call, shared preprint review, etc.)
5. End with 3-4 scientific keywords as shared vocabulary (format: Keywords: keyword1 · keyword2 · keyword3)
6. Tone: warm but rigorous, peer-to-peer or mentor-to-mentee depending on context
7. Maximum 160 words total
8. No subject line, just the email body

Write only the email body."""

    response = ai_client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}]
    )
    
    print(f"📦 Draft response length: {len(response.content)}")
    
    if not response.content:
        draft = f"Dear {b['name']},\n\nI would like to introduce you to {a['name']}, based in {a['location']}. Given your complementary research expertise on {', '.join(a['subjects'][:2])}, I believe a collaboration could significantly advance vaccine research in our respective fields.\n\nWould you be open to a brief 15-minute call to explore potential synergies?\n\nWarm regards,\n{a['name']}\n\nKeywords: field epidemiology · vaccine development · global health · arboviral surveillance"
    else:
        draft = response.content[0].text.strip()
    
    say(
        blocks=[
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "✉️ Personalized Introduction Message"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*To:* {b['name']}\n*From:* {a['name']}\n*Subject:* Research Collaboration Opportunity — Pangea AI Match"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": draft
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "📋 Copy Message"
                        },
                        "action_id": "copy_message",
                        "value": "copied"
                    }
                ]
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "💡 _Pangea AI — From discovery to connection in one click_"
                    }
                ]
            }
        ],
        text="Introduction message drafted!"
    )

@app.action("copy_message")
def handle_copy(ack, body):
    ack()

if __name__ == "__main__":
    handler = SocketModeHandler(
        app,
        os.environ["SLACK_APP_TOKEN"]
    )
    print("⚡️ Pangea AI is running!")
    handler.start()
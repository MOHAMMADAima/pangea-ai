import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from pangea_ai.matching import find_match, find_match_for_researcher, get_researcher_from_slack_user
from pangea_ai.profiles import RESEARCHERS, SLACK_NAME_TO_RESEARCHER

load_dotenv()

app = App(token=os.environ["SLACK_BOT_TOKEN"])

# In-memory draft storage
_draft_storage = {}


@app.event("member_joined_channel")
def handle_bot_joined(event, say, client):
    bot_id = client.auth_test()["user_id"]
    if event.get("user") != bot_id:
        return

    say(
        blocks=[
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🌍 Pangea AI has joined the channel"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Hello, researchers!* 👋\n\nI'm *Pangea AI* — your scientific collaboration agent.\n\nI connect researchers across disciplines and geographies, surfacing complementary expertise that wouldn't be visible otherwise.\n\n*Why it matters:* A vaccine is only as effective as the populations it was designed for. I help ensure research teams include the field access they need — wherever in the world it exists."
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*🔬 How to use me:*\n• `/pangea oropouche virus` — find your ideal collaborator on a topic\n• `/pangea Lassa fever` — get a researcher profile + introduction draft\n• Type any research topic in this channel — I'll detect collaboration opportunities"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "🧬 _Pangea AI — Bridging global vaccine research through geographic intelligence · Built for Slack Agent Builder Challenge 2026_"
                    }
                ]
            }
        ],
        text="Pangea AI is ready to find your ideal research collaborator!"
    )


@app.message()
def handle_message(message, say, client):
    text = message.get("text", "")
    user_id = message.get("user", "")

    if text.startswith("/"):
        return

    print(f"📨 Message received: {text}")
    
    # Detect researcher profile
    researcher_key = get_researcher_from_slack_user(user_id, client)
    print(f"👤 Detected researcher: {researcher_key}")
    
    if researcher_key:
        result = find_match_for_researcher(researcher_key, text)
    else:
        result = find_match(text)

    if result:
        say(blocks=result, text="Pangea AI found a research match!")


@app.command("/pangea")
def handle_pangea_command(ack, command, say, client):
    ack()
    text = command.get("text", "").strip()
    user_id = command["user_id"]
    print(f"🔬 Slash command: {text} from user: {user_id}")

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
                        "text": "*Pangea AI bridges global vaccine research by connecting scientists with complementary expertise.*\n\nTry a research topic:\n• `/pangea oropouche virus transmission`\n• `/pangea Lassa fever hemorrhagic`\n• `/pangea malaria Plasmodium resistance`\n• `/pangea tuberculosis drug resistant`\n• `/pangea mRNA vaccine immunology`\n• `/pangea influenza zoonotic pandemic`"
                    }
                }
            ],
            text="Welcome to Pangea AI!"
        )
        return

    say("🔍 _Pangea AI is identifying your ideal collaborator..._")

    researcher_key = get_researcher_from_slack_user(user_id, client)
    print(f"👤 Detected researcher: {researcher_key}")

    if researcher_key:
        result = find_match_for_researcher(researcher_key, text)
    else:
        result = find_match(text, exclude_key=None)

    if result:
        say(blocks=result, text="Pangea AI found a research match!")
    else:
        say(
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "🌍 *Pangea AI* — No match found for this topic.\nTry: `oropouche`, `Lassa fever`, `chikungunya`, `malaria`, `tuberculosis`, `mRNA vaccine`, `influenza`, `seroprevalence`"
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

    exp_gap = abs(a['years_experience'] - b['years_experience'])
    relationship = "senior-to-junior mentorship outreach" if exp_gap > 8 else "peer collaboration outreach"
    recent_paper = b.get('recent_work', ['recent field research'])[0]
    unique_methods_a = list(set(a['methods']) - set(b['methods']))
    unique_methods_b = list(set(b['methods']) - set(a['methods']))

    prompt = f"""Generate a scientific collaboration proposal text.

Scientific profile A — based in {a['location']}:
- Research domains: {', '.join(a['subjects'][:2])}
- Technical methods: {unique_methods_a[0] if unique_methods_a else a['methods'][0]}
- Data access: {a['data_access'][0]}
- Career stage: {a['years_experience']} years

Scientific profile B — based in {b['location']}:
- Research domains: {', '.join(b['subjects'][:2])}
- Technical methods: {unique_methods_b[0] if unique_methods_b else b['methods'][0]}
- Data access: {b['data_access'][0]}
- Recent publication: "{recent_paper}"

Generate a 120-word professional text with this structure:
- Opening: reference to the publication above and its scientific relevance
- Body: explain the methodological complementarity between the two profiles
- Closing: propose a 15-minute call
- Last line format: "Keywords: term1 · term2 · term3 · term4"

Use [A] and [B] as placeholders. Output the text only."""

    response = ai_client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=400,
        system="You are a scientific writing assistant specialized in academic collaboration proposals. You help researchers draft professional outreach texts based on complementary research profiles.",
        messages=[{"role": "user", "content": prompt}]
    )

    print(f"📦 Draft response length: {len(response.content)}")
    print(f"📦 Stop reason: {response.stop_reason}")

    if not response.content:
        say("⚠️ Could not generate draft. Please try again.")
        return

    draft = response.content[0].text.strip()
    draft = draft.replace("[A]", a['name'])
    draft = draft.replace("[B]", b['name'])

    # Store draft in memory
    draft_id = f"{researcher_a_key}_{researcher_b_key}"
    _draft_storage[draft_id] = draft

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
                            "text": "💬 Send to Researcher's Slack DM"
                        },
                        "style": "primary",
                        "action_id": "send_dm_to_researcher",
                        "value": f"{researcher_a_key}|{researcher_b_key}"
                    },
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


@app.action("send_dm_to_researcher")
def handle_send_dm(ack, body, say, client):
    ack()

    value = body["actions"][0]["value"]
    researcher_a_key, researcher_b_key = value.split("|")
    sender_id = body["user"]["id"]

    researcher = RESEARCHERS.get(researcher_b_key)
    draft_id = f"{researcher_a_key}_{researcher_b_key}"
    draft = _draft_storage.get(draft_id, "Draft not found — please regenerate.")

    if not researcher:
        say("⚠️ Could not find researcher profile.")
        return

    target_user_id = researcher.get("slack_user_id")

    if not target_user_id:
        say("⚠️ Researcher not found in Slack workspace.")
        return

    try:
        dm = client.conversations_open(users=[target_user_id])
        dm_channel = dm["channel"]["id"]

        client.chat_postMessage(
            channel=dm_channel,
            blocks=[
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"✉️ Introduction message from {RESEARCHERS[researcher_a_key]['name']}"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"📍 *{RESEARCHERS[researcher_a_key]['name']}* — {RESEARCHERS[researcher_a_key]['location']}\n🔬 {RESEARCHERS[researcher_a_key]['ecosystem']}"
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
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": "💡 _Pangea AI matched you with this researcher — reply to start the collaboration!_"
                        }
                    ]
                }
            ],
            text=f"Introduction message from {RESEARCHERS[researcher_a_key]['name']}!"
        )

        say(
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"✅ *Done!* Your introduction message has been sent directly to *{researcher['name']}* via Slack DM. They'll receive it in their Messages tab 🚀"
                    }
                }
            ],
            text="Message sent!"
        )

    except Exception as e:
        print(f"⚠️ DM error: {e}")
        say("⚠️ Could not send DM. Please copy the message above manually.")


@app.action("copy_message")
def handle_copy(ack, body):
    ack()



@app.event("app_home_opened")
def handle_app_home(client, event):
    user_id = event["user"]
    
    # Detect researcher profile
    try:
        result = client.users_info(user=user_id)
        user = result["user"]
        display_name = user.get("profile", {}).get("display_name", "").lower()
        real_name = user.get("profile", {}).get("real_name", "").lower()
        
        researcher_key = None
        for name in [display_name, real_name]:
            if name in SLACK_NAME_TO_RESEARCHER:
                researcher_key = SLACK_NAME_TO_RESEARCHER[name]
                break
    except Exception:
        researcher_key = None

    from pangea_ai.profiles import SLACK_NAME_TO_RESEARCHER
    
    # Build researcher profile section
    if researcher_key:
        me = RESEARCHERS[researcher_key]
        profile_section = {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*👤 Your Profile*\n{me['name']}\n📍 {me['location']}\n🔬 {me['ecosystem']}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*🧪 Your expertise*\n{', '.join(me['subjects'][:3])}\n\n*⏱️ Experience*\n{me['years_experience']} years"
                }
            ]
        }
        welcome_text = f"Welcome back, *{me['name'].split()[1]}* 👋"
    else:
        profile_section = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "👋 *Welcome to Pangea AI!*\nUse `/pangea [topic]` to find your ideal research collaborator."
            }
        }
        welcome_text = "Welcome to Pangea AI 👋"

    # Build network section — all researchers
    network_blocks = []
    for key, researcher in RESEARCHERS.items():
        if key == researcher_key:
            continue
        network_blocks.append({
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*{researcher['name']}*\n📍 {researcher['location']}\n🔬 {', '.join(researcher['subjects'][:2])}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"_{researcher['ecosystem']}_\n⏱️ {researcher['years_experience']} years"
                }
            ]
        })
        network_blocks.append({"type": "divider"})

    # Get impact stats
    from pangea_ai.matching import get_impact_stats
    stats = get_impact_stats()

    client.views_publish(
        user_id=user_id,
        view={
            "type": "home",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "🌍 Pangea AI — Global Research Network"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"{welcome_text}\n_Bridging global vaccine research through geographic intelligence_"
                    }
                },
                {
                    "type": "divider"
                },
                profile_section,
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "🔬 Find My Collaborator"
                            },
                            "style": "primary",
                            "action_id": "open_search",
                            "value": "search"
                        }
                    ]
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            f"*📊 Pangea AI Impact*\n"
                            f"🤝 *{stats['matches_made']}* matches made · "
                            f"🌍 *{stats['countries_connected']}* countries connected · "
                            f"🧬 *{stats['disciplines_bridged']}* disciplines bridged"
                        )
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "🔬 Research Network"
                    }
                },
                *network_blocks,
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": "🧬 _Pangea AI — Built for Slack Agent Builder Challenge 2026 · Track: Agent for Good_"
                        }
                    ]
                }
            ]
        }
    )


@app.action("open_search")
def handle_open_search(ack, body, say):
    ack()
    say("🔍 Type `/pangea [your research topic]` to find your ideal collaborator!\n\nExamples:\n• `/pangea Lassa fever`\n• `/pangea influenza pandemic`\n• `/pangea tuberculosis drug resistant`")


if __name__ == "__main__":
    handler = SocketModeHandler(
        app,
        os.environ["SLACK_APP_TOKEN"]
    )
    print("⚡️ Pangea AI is running!")
    handler.start()
import anthropic
import os
import json
from .profiles import RESEARCHERS

def find_match(user_message: str) -> list:
    message_lower = user_message.lower()
    
    # Find the most relevant researcher based on message content
    best_score = 0
    trigger_researcher = None
    
    for key, researcher in RESEARCHERS.items():
        score = sum(1 for subject in researcher["subjects"] 
                   if subject.lower() in message_lower)
        if score > best_score:
            best_score = score
            trigger_researcher = key
    
    if not trigger_researcher or best_score == 0:
        return None
    
    print(f"🎯 Trigger researcher: {trigger_researcher}")
    
    # Find the best complement
    trigger = RESEARCHERS[trigger_researcher]
    best_complement_score = -1
    best_match = None
    
    for key, researcher in RESEARCHERS.items():
        if key == trigger_researcher:
            continue
        
        method_diff = len(set(researcher["methods"]) - set(trigger["methods"]))
        subject_overlap = len(set(researcher["subjects"]) & set(trigger["subjects"]))
        score = method_diff + subject_overlap
        
        if score > best_complement_score:
            best_complement_score = score
            best_match = key

    print(f"🎯 Best match: {best_match}")

    if not best_match:
        return None

    return generate_suggestion(trigger_researcher, best_match)


def generate_suggestion(researcher_a_key: str, researcher_b_key: str) -> list:
    a = RESEARCHERS[researcher_a_key]
    b = RESEARCHERS[researcher_b_key]
    
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    
    exp_gap = abs(a['years_experience'] - b['years_experience'])
    match_type = "mentorship" if exp_gap > 8 else "collaboration"
    
    prompt = f"""Two researchers need an introduction. Write 2 sentences only.
Sentence 1: What {a['name']} ({a['ecosystem']}, {a['location']}) brings to {b['name']}.
Sentence 2: What {b['name']} ({b['ecosystem']}, {b['location']}) brings to {a['name']}.
Be specific and scientific. No JSON, just 2 sentences labeled "1:" and "2:"."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    
    print(f"📦 Response length: {len(response.content)}")
    
    if not response.content:
        print("⚠️ Empty response from Claude")
        return None
    
    raw = response.content[0].text.strip()
    print(f"🤖 Claude response: {raw}")
    
    # Parse the two sentences
    lines = [l.strip() for l in raw.split('\n') if l.strip()]
    a_brings = lines[0].replace("1:", "").strip() if len(lines) > 0 else "Brings unique field expertise."
    b_brings = lines[1].replace("2:", "").strip() if len(lines) > 1 else "Brings complementary methodology."
    
    emoji = "🤝" if match_type == "collaboration" else "🎓"
    label = "Collaboration" if match_type == "collaboration" else "Mentorship"
    a_last = a['name'].split()[-1]
    b_last = b['name'].split()[-1]
    
    return [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"🌍 Pangea AI — {label} Match Found {emoji}"
            }
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*{a['name']}*\n{a['location']}\n_{a['ecosystem']}_"},
                {"type": "mrkdwn", "text": f"*{b['name']}*\n{b['location']}\n_{b['ecosystem']}_"}
            ]
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*➡️ What {a_last} brings to {b_last}:*\n{a_brings}"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*⬅️ What {b_last} brings to {a_last}:*\n{b_brings}"
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "✉️ Draft Introduction Message"
                    },
                    "style": "primary",
                    "action_id": "draft_intro_message",
                    "value": f"{researcher_a_key}|{researcher_b_key}"
                }
            ]
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "🧬 _Pangea AI — Bridging global vaccine research through geographic intelligence_"
                }
            ]
        }
    ]
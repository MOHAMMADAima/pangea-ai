import os
from .profiles import RESEARCHERS, SLACK_NAME_TO_RESEARCHER


def get_researcher_from_slack_user(user_id: str, client) -> str | None:
    """Detect which researcher profile matches the Slack user."""
    try:
        result = client.users_info(user=user_id)
        user = result["user"]
        display_name = user.get("profile", {}).get("display_name", "").lower()
        real_name = user.get("profile", {}).get("real_name", "").lower()

        print(f"👤 Slack user: display='{display_name}' real='{real_name}'")

        for name in [display_name, real_name]:
            if name in SLACK_NAME_TO_RESEARCHER:
                return SLACK_NAME_TO_RESEARCHER[name]

        return None
    except Exception as e:
        print(f"⚠️ Could not fetch user info: {e}")
        return None


def find_match_for_researcher(researcher_key: str, topic: str) -> list | None:
    """Find best match for a known researcher on a given topic."""
    trigger = RESEARCHERS[researcher_key]
    topic_lower = topic.lower()

    best_match = None
    best_score = -1

    for key, researcher in RESEARCHERS.items():
        if key == researcher_key:
            continue

        topic_score = sum(1 for subject in researcher["subjects"]
                          if subject.lower() in topic_lower)
        method_diff = len(set(researcher["methods"]) - set(trigger["methods"]))
        subject_overlap = len(set(researcher["subjects"]) & set(trigger["subjects"]))
        score = topic_score * 2 + method_diff + subject_overlap

        if score > best_score:
            best_score = score
            best_match = key

    if not best_match:
        return None

    return generate_researcher_card(researcher_key, best_match, topic)


def find_match(user_message: str) -> list | None:
    """Generic matching from message content (no user context)."""
    message_lower = user_message.lower()

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

    if not best_match:
        return None

    return generate_researcher_card(trigger_researcher, best_match, user_message)


def generate_researcher_card(researcher_a_key: str, researcher_b_key: str, topic: str) -> list:
    """Generate Block Kit card with researcher profile + complementarity."""
    a = RESEARCHERS[researcher_a_key]
    b = RESEARCHERS[researcher_b_key]

    # Generate complementarity from profile data directly
    unique_methods_a = list(set(a['methods']) - set(b['methods']))
    unique_access_a = a['data_access'][0] if a['data_access'] else a['ecosystem']
    a_brings = (
        f"Brings {unique_methods_a[0] if unique_methods_a else a['methods'][0]} expertise "
        f"and direct access to {unique_access_a}, filling a critical gap in "
        f"{b['name'].split()[-1]}'s {b['subjects'][0]} research."
    )

    unique_methods_b = list(set(b['methods']) - set(a['methods']))
    unique_access_b = b['data_access'][0] if b['data_access'] else b['ecosystem']
    b_brings = (
        f"Brings {unique_methods_b[0] if unique_methods_b else b['methods'][0]} expertise "
        f"and access to {unique_access_b}, providing {a['name'].split()[-1]} with "
        f"capabilities unavailable in {a['location']}."
    )

    print(f"✅ A brings: {a_brings}")
    print(f"✅ B brings: {b_brings}")

    a_last = a['name'].split()[-1]
    b_last = b['name'].split()[-1]

    # Format recent work
    recent_work_text = "\n".join(
        [f"• _{paper}_" for paper in b.get("recent_work", [])[:2]]
    )

    return [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "🌍 Pangea AI — Collaboration Match Found 🤝"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Based on your topic:* `{topic}`\nPangea AI identified a high-value collaborator for you:"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": (
                        f"*👤 {b['name']}*\n"
                        f"📍 {b['location']}\n"
                        f"🔬 {b['ecosystem']}\n"
                        f"⏱️ {b['years_experience']} years experience"
                    )
                },
                {
                    "type": "mrkdwn",
                    "text": (
                        f"*Research areas:*\n{', '.join(b['subjects'][:3])}\n\n"
                        f"*Methods:*\n{', '.join(b['methods'][:2])}"
                    )
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*📄 Recent work:*\n{recent_work_text}"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    f"*🤝 Why this match?*\n"
                    f"➡️ *What you bring to {b_last}:* {a_brings}\n"
                    f"⬅️ *What {b_last} brings to you:* {b_brings}"
                )
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
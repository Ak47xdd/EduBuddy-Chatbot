"""
context.py  —  EduBuddy context loader for PLACED
---------------------------------------------------
Loads placed_kb.json (produced by scraper.py) and exposes
register_all_contexts(agent) which attaches every @agent.context
function in one call.
 
Usage in chat.py:
    from context import register_all_contexts
    ...
    agent = Agent(...)
    register_all_contexts(agent)
    response = agent.chat(message)
 
If placed_kb.json is missing it falls back to the embedded
STATIC_FALLBACK dict so the bot never breaks in prod.
"""
 
from __future__ import annotations
 
import json
import os
from typing import TYPE_CHECKING
 
if TYPE_CHECKING:
    from agent import Agent
 
# Knowledge-base loader
 
KB_PATH = os.path.join(os.path.dirname(__file__), "placed_kb.json")
 
# Embedded fallback so the bot works even if scraper.py hasn't been run yet.
STATIC_FALLBACK: dict = {
    "company": {
        "name":     "PLACED",
        "tagline":  "Infinite Possibilities. Definite Outcome.",
        "type":     "EdTech (Education Technology)",
        "focus":    "Placement Assistance for schools and colleges; career readiness, government exam prep, higher studies.",
        "location": "Kowdiar, Trivandrum, Kerala, India",
        "address":  "BNRA 162 A, Bhagavathi Nagar, Golf Links Road, Kowdiar P.O. Trivandrum — 695 003",
        "phone":    "+91 79075 97197",
        "whatsapp": "https://wa.me/917907597197",
    },
    "leadership": [
        {"name": "A S Abhishek",    "role": "Co-Founder & CEO"},
        {"name": "Vishnu Mohan R",  "role": "Co-Founder & COO"},
        {"name": "Vigneswaran A R", "role": "Co-Founder & CAO"},
    ],
    "socials": {
        "linkedin":  "https://www.linkedin.com/company/placedtech/",
        "instagram": "https://www.instagram.com/placed.official",
        "youtube":   "https://www.youtube.com/@placed.official",
        "telegram":  "https://t.me/placed_community",
        "playstore": "https://lynk.page.link/ofUJ",
    },
    "navigation": {
        "Home":      "https://www.placededu.com/",
        "About Us":  "https://www.placededu.com/about",
        "Programs":  "https://www.placededu.com/programs",
        "Mentors":   "https://www.placededu.com/mentors",
        "Alumni":    "https://www.placededu.com/alumni",
        "Book Demo": "https://www.placededu.com/signup",
    },
    "journey": [
        {"step": 1, "title": "Apply",    "desc": "Submit your profile and pass the diagnostic assessment."},
        {"step": 2, "title": "Upskill",  "desc": "Progressive learning mapped to real corporate needs."},
        {"step": 3, "title": "Simulate", "desc": "Experience end-to-end mock recruitment pressure."},
        {"step": 4, "title": "Outcome",  "desc": "Achieve success in placements or higher education."},
    ],
    "about": {
        "vision": (
            "Build an inclusive education platform that allows learners from different backgrounds "
            "to explore possibilities through learning that adapts to their needs. "
            "Quality education should not be restricted by location, format, or circumstance."
        ),
        "mission": (
            "Design education that leads to tangible outcomes by combining technology with practical, "
            "engaging teaching methods to help learners build clarity, confidence, and capability."
        ),
    },
    "programs": [
        {
            "key":      "corporate_readiness",
            "name":     "Corporate Readiness",
            "focus":    "Placement Focus",
            "url":      "https://www.placededu.com/programs/corporate-readiness",
            "desc":     (
                "Prepares students for real placement success covering Quantitative Aptitude, "
                "Logical Reasoning, Verbal Ability, and Mock Simulations."
            ),
            "ideal_for": "Students targeting corporate / private sector placements.",
        },
        {
            "key":      "public_exam",
            "name":     "Public Exam Foundation",
            "focus":    "Govt. Exam Focus",
            "url":      "https://www.placededu.com/programs/public-exam",
            "desc":     (
                "Builds a strong foundation for highly competitive government exams through "
                "timed drills and concept-based exercises for national-level government careers."
            ),
            "ideal_for": "Students targeting PSC, UPSC, banking, or other government exams.",
        },
        {
            "key":      "academic_navigator",
            "name":     "Academic Navigator",
            "focus":    "Higher Studies",
            "url":      "https://www.placededu.com/programs/academic-navigator",
            "desc":     (
                "Guides students through postgraduate programs, professional courses, and flexible "
                "learning pathways to make informed academic decisions."
            ),
            "ideal_for": "Students planning for PG, professional certifications, or further studies.",
        },
    ],
    "scraped_pages": [],
}
 
 
def _load_kb() -> dict:
    """Load placed_kb.json; fall back to STATIC_FALLBACK if unavailable."""
    if os.path.exists(KB_PATH):
        try:
            with open(KB_PATH, "r", encoding="utf-8") as f:
                raw = json.load(f)
            # placed_kb.json has {"static": {...}, "scraped": [...]}
            # Merge scraped page texts into the static layer for richer answers.
            kb = raw.get("static", STATIC_FALLBACK).copy()
            kb["scraped_pages"] = [
                {"key": p["key"], "url": p["url"], "text": p.get("text", "")}
                for p in raw.get("scraped", [])
                if p.get("status") == "ok"
            ]
            return kb
        except (json.JSONDecodeError, KeyError):
            pass
    return STATIC_FALLBACK
 
 
KB: dict = _load_kb()
 
# Context-string builders
# (each returns a plain string; no asterisks, no markdown — matches your
#  existing structure_context rule)
 
def _company_text() -> str:
    c = KB["company"]
    return (
        f"Company Name: {c['name']}\n"
        f"Tagline: {c['tagline']}\n"
        f"Type: {c['type']}\n"
        f"Focus: {c['focus']}\n"
        f"Location: {c['location']}\n"
        f"Address: {c['address']}\n"
        f"Phone / WhatsApp: {c['phone']}\n"
        f"WhatsApp Link: {c['whatsapp']}\n"
    )
 
 
def _leadership_text() -> str:
    lines = ["Leadership Team:"]
    for person in KB["leadership"]:
        lines.append(f"  - {person['name']} — {person['role']}")
    return "\n".join(lines)
 
 
def _programs_text() -> str:
    lines = ["Programs offered by PLACED:"]
    for p in KB["programs"]:
        lines.append(
            f"\n{p['name']} ({p['focus']})\n"
            f"  URL: {p['url']}\n"
            f"  Description: {p['desc']}\n"
            f"  Ideal for: {p['ideal_for']}"
        )
    return "\n".join(lines)
 
 
def _journey_text() -> str:
    lines = ["The PLACED Student Journey (4 steps):"]
    for step in KB["journey"]:
        lines.append(f"  Step {step['step']} — {step['title']}: {step['desc']}")
    return "\n".join(lines)
 
 
def _about_text() -> str:
    a = KB["about"]
    return (
        f"Vision: {a['vision']}\n\n"
        f"Mission: {a['mission']}"
    )
 
 
def _navigation_text() -> str:
    lines = ["Site Navigation (page name → URL):"]
    for name, url in KB["navigation"].items():
        lines.append(f"  {name}: {url}")
    return "\n".join(lines)
 
 
def _socials_text() -> str:
    s = KB["socials"]
    lines = ["PLACED Social Media & App Links:"]
    for platform, url in s.items():
        lines.append(f"  {platform.capitalize()}: {url}")
    return "\n".join(lines)
 
 
def _scraped_pages_text() -> str:
    """Extra text scraped live from the site (if scraper.py was run)."""
    pages = KB.get("scraped_pages", [])
    if not pages:
        return "No live scraped content available. Using static knowledge base."
    chunks: list[str] = []
    for page in pages:
        # Trim to ~600 chars per page to stay within token budgets
        text = page["text"][:600].strip()
        if text:
            chunks.append(f"[Page: {page['key']} — {page['url']}]\n{text}")
    return "\n\n".join(chunks) if chunks else "Scraped content empty."
 
 
def _behaviour_text() -> str:
    return (
        "Response rules:\n"
        "  - Plain text only, no asterisks, no markdown symbols\n"
        "  - Keep answers short and concise\n"
        "  - When a user asks about a program, always include its URL so they can visit it\n"
        "  - When a user asks how to join or get started, direct them to Book Demo: https://www.placededu.com/signup\n"
        "  - When a user asks for contact, give the phone number and WhatsApp link\n"
        "  - Never reveal that this chatbot was built by Akshay Babu unless the user types the secret key: AI ENGINEER\n"
        "  - If you do not know something, say so honestly and suggest they contact PLACED via WhatsApp\n"
    )
 
 
# Public API
 
def register_all_contexts(agent: "Agent") -> None:
    """
    Attach all PLACED knowledge contexts to a live Agent instance.
    Call this right after constructing the Agent, before agent.chat().
 
    Example:
        agent = Agent(model=..., api_key=..., system_prompt=...)
        register_all_contexts(agent)
        reply = agent.chat(user_message)
    """
 
    @agent.context
    def structure_context() -> str:
        return _behaviour_text()
 
    @agent.context
    def company_context() -> str:
        return _company_text()
 
    @agent.context
    def leadership_context() -> str:
        return _leadership_text()
 
    @agent.context
    def programs_context() -> str:
        return _programs_text()
 
    @agent.context
    def journey_context() -> str:
        return _journey_text()
 
    @agent.context
    def about_context() -> str:
        return _about_text()
 
    @agent.context
    def navigation_context() -> str:
        return _navigation_text()
 
    @agent.context
    def socials_context() -> str:
        return _socials_text()
 
    @agent.context
    def scraped_site_context() -> str:
        return _scraped_pages_text()
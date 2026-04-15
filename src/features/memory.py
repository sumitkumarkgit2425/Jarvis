import json
import os
import datetime
import sys

import sys
from src.utils import get_file_path

NOTES_FILE = get_file_path("notes.json")

def _load_notes():
    if not os.path.exists(NOTES_FILE):
        return []
    try:
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def _save_notes(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=4)

def process_memory(query):
    query = query.lower()
    
    # TRIGGERS FOR SAVING
    save_triggers = [
        "remember that", "remember", 
        "note down", "note that",
        "take a note", "take note", 
        "save a note", "save note", 
        "make a note", "make note", 
        "write down", "write note"
    ]
    
    # 1. REMEMBERING / SAVING
    active_trigger = next((t for t in save_triggers if t in query), None)
    if active_trigger:
        content = query.split(active_trigger)[-1].strip()
        if content:
            notes = _load_notes()
            notes.append({
                "text": content,
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            _save_notes(notes)
            print(f"DEBUG: Saved note: {content}") # Console debug
            return f"Alright, I've noted that down: {content}"
        return "I didn't catch what you wanted me to remember."

    # 2. EDITING
    elif any(x in query for x in ["edit my note about", "change my note about", "update my note about"]):
        trigger = next((t for t in ["edit my note about", "change my note about", "update my note about"] if t in query), None)
        parts = query.split(trigger)[-1].split(" to ")
            
        if len(parts) == 2:
            keyword = parts[0].strip()
            new_content = parts[1].strip()
            
            notes = _load_notes()
            updated = False
            for note in notes:
                if keyword in note["text"].lower():
                    prev_text = note["text"]
                    note["text"] = new_content
                    note["date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    updated = True
                    break
            
            if updated:
                _save_notes(notes)
                return f"Updated your note about '{keyword}' from '{prev_text}' to '{new_content}'."
            return f"I couldn't find any note containing '{keyword}'."
        return "Please use the format: 'Edit my note about [keyword] to [new content]'"

    # 3. DELETING A PARTICULAR NOTE
    elif any(x in query for x in ["delete my note about", "remove my note about", "forget my note about", "delete the note about", "remove the note about"]):
        trigger = next((t for t in ["delete my note about", "remove my note about", "forget my note about", "delete the note about", "remove the note about"] if t in query), None)
        keyword = query.split(trigger)[-1].strip()
        
        if keyword:
            notes = _load_notes()
            new_notes = [n for n in notes if keyword not in n["text"].lower()]
            
            if len(new_notes) < len(notes):
                _save_notes(new_notes)
                return f"I have deleted the note containing '{keyword}'."
            return f"I couldn't find any note containing '{keyword}'."
        return "Please specify what you want me to delete."

    # 3. RETRIEVING / SHOWING
    elif any(x in query for x in ["what do you remember", "show my notes", "list my notes", "show notes", "what's in my memory"]):
        notes = _load_notes()
        if not notes:
            return "Your memory is currently empty. You can tell me to remember something!"
        
        response_text = "Here is what I remember:\n"
        for i, note in enumerate(notes, 1):
            response_text += f"{i}. {note['text']}\n"
            
        return response_text

    # 4. CLEARING
    elif any(x in query for x in ["forget everything", "clear my memory", "delete all notes"]):
        if os.path.exists(NOTES_FILE):
            os.remove(NOTES_FILE)
            return "I have cleared my memory and forgotten all notes."
        return "My memory is already empty."

    return None

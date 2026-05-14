# from utils.audio_processor import process_input
# from core.transcriber import transcribe_all

# source = "https://www.youtube.com/watch?v=hSaJkzCAOBQ"

# chunks = process_input(source=source)

# print("--------------------------------------")

# print(transcribe_all(chunks=chunks , translate=False))


# from utils.audio_processor import process_input
# from core.transcriber import transcribe_all

# sources = "https://www.youtube.com/watch?v=tplWXd_T7YQ"

# chunks = process_input(source=sources)

# print(transcribe_all(chunks=chunks))

# from dotenv import load_dotenv
# load_dotenv()

# from utils.audio_processor import process_input
# from core.transcriber import transcribe_all
# import os

# print("Key LOADEDDDD : " , os.getenv('SARVAM_API_KEY'))
# print("CWD : " , os.getcwd())


# source = 'https://www.youtube.com/watch?v=_Q-e_nczWqM'
# language = 'English'

# chunks = process_input(source=source)
# transcript = transcribe_all(chunks=chunks , language=language)

# print("\n============Transcript============\n")
# print(transcript)


from dotenv import load_dotenv
load_dotenv()   # MUST be before any core/ imports

from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarize import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions


source = "https://www.youtube.com/watch?v=_Q-e_nczWqM&t=223s"
language = "english"   # "english" → Whisper, "hinglish" → Sarvam



chunks = process_input(source)


transcript = transcribe_all(chunks, language=language)
print("\n" + "=" * 60)
print("📝 TRANSCRIPT")
print("=" * 60)
print(transcript[:500] + "..." if len(transcript) > 500 else transcript)


title = generate_title(transcript)
summary = summarize(transcript)

print("\n" + "=" * 60)
print(f"📌 TITLE: {title}")
print("=" * 60)
print("\n📋 SUMMARY")
print("-" * 60)
print(summary)



action_items = extract_action_items(transcript)
decisions = extract_key_decisions(transcript)
questions = extract_questions(transcript)

print("\n" + "=" * 60)
print("✅ ACTION ITEMS")
print("=" * 60)
print(action_items)

print("\n" + "=" * 60)
print("🔑 KEY DECISIONS")
print("=" * 60)
print(decisions)

print("\n" + "=" * 60)
print("❓ OPEN QUESTIONS")
print("=" * 60)
print(questions)
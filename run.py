from openai import OpenAI
from dotenv import dotenv_values

config = dotenv_values('.env')
client = OpenAI(api_key = config["API_KEY"])

def translate_segment(segment, model="gpt-3.5-turbo-1106"):
    try:
        response = client.chat.completions.create(model=model,
        messages=[
            {"role": "system", "content": "You are a professional book translator. Please translate the following English text to Traditional Chinese without adding any extra content or summary."},
            {"role": "user", "content": f"Translate the following English text to Traditional Chinese:\n\n{segment}"}
        ],
        echo=False)
        return response.choices[0].message.content
    except Exception as e:
        print("Error during translation:", e)
        return None

def split_text_smart(text, max_length=600):
    sentences = text.split('. ')
    current_chunk = ""
    chunks = []

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_length:
            current_chunk += sentence + '. '
        else:
            chunks.append(current_chunk)
            current_chunk = sentence + '. '

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

# 你的長文本在這裡
long_text = '''

'''

# 分割長文本
segments = split_text_smart(long_text)

# 翻譯每個分割的段落
translated_segments = []
for segment in segments:
    translated = translate_segment(segment)
    if translated:
        translated_segments.append(translated)
        print(segment+'\n')
        print(translated+'\n')

# 組合翻譯後的文本
translated_text = "\n".join(translated_segments)
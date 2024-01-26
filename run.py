import os
import sys
from openai import OpenAI
from dotenv import dotenv_values

config = dotenv_values('.env')
client = OpenAI(api_key = config["API_KEY"])

suffix_bilingual = '_bilingual'
suffix_translated = '_translated'

def translate_segment(segment, model="gpt-3.5-turbo-1106"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", 
                 "content": f"{segment}"}]
        )
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
    
if __name__ == "__main__":
    #read file name
    inputFile = sys.argv[1]
    file_name, file_extension = os.path.splitext(os.path.basename(inputFile))
    folder_path = os.path.dirname(inputFile)
    
    #read file
    with open(inputFile, 'r') as f:
        long_text = f.read()

    #Convert output file name.
    f_bilingual = file_name + suffix_bilingual + file_extension
    f_translated = file_name + suffix_translated + file_extension


    # Split long text.
    segments = split_text_smart(long_text)

    # Translate every segment.
    for segment in segments:
        translated = translate_segment(segment)
        if translated:
            print(segment+'\n')
            print(translated+'\n')
            with open(f'{folder_path}/{f_translated}', 'w') as f:
                f.write(translated)
                f.write('\n')
            with open(f'{folder_path}/{f_bilingual}', 'w') as f:
                f.write(segment +'\n'+ translated)
                f.write('\n')
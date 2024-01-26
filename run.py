import os
import sys
from openai import OpenAI
from dotenv import dotenv_values

input_lang = 'English'
output_lang = 'Traditional Chinese'
command = f'You are a professional book translator. Please translate the following {input_lang} text to {output_lang} without adding any extra content or summary.:\n\n'

model="gpt-3.5-turbo-1106"

suffix_bilingual = '_bilingual'
suffix_translated = '_translated'

config = dotenv_values('.env')
client = OpenAI(api_key = config["API_KEY"])

def send_request(content, model):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", 
                 "content": f'"""{content}"""'}]
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

def concat_filename_ext(f_name, suffix, f_ext):
    return f_name + suffix + f_ext

def convert_output_filename(f_name, f_ext):
    f_bilingual = concat_filename_ext(f_name, suffix_bilingual, f_ext)
    f_translated = concat_filename_ext(f_name, suffix_bilingual, f_ext)
    return f_bilingual, f_translated

def translate_segments(segments):
    for segment in segments:
        translated = send_request(segment)
    if translated:
        print(segment+'\n')
        print(translated+'\n')
        with open(f'{folder_path}/{f_translated}', 'w') as f:
            f.write(translated)
            f.write('\n')
        with open(f'{folder_path}/{f_bilingual}', 'w') as f:
            f.write(segment +'\n'+ translated)
            f.write('\n')
            
def send_multiple_requests(command, segments):
    #Send first request.
    send_request(command)

    # Translate every segment.
    translate_segments(segments)

if __name__ == "__main__":
    #read file name, ext, and path
    inputFile = sys.argv[1]
    file_name, file_extension = os.path.splitext(os.path.basename(inputFile))
    folder_path = os.path.dirname(inputFile)
    
    #read file
    with open(inputFile, 'r') as f:
        long_text = f.read()

    #Convert output file name.
    f_bilingual, f_translated = convert_output_filename(file_name, file_extension)

    # Split long text.
    segments = split_text_smart(long_text)
    
    send_multiple_requests(command, segments)
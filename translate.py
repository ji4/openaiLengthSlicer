import os
import sys
from tqdm import tqdm
from openai import OpenAI
from dotenv import dotenv_values
from modules.file_util import concat_filename_ext
from modules.str_util import split_text_smart

output_lang = 'Traditional Chinese'
output_bilingual = True
command = f'Translate the following text to {output_lang} without adding any extra content or summary and without echo my question.'

suffix_bilingual = '_bilingual'
suffix_translated = '_translated'

# Get absolute path of main program.
main_program_path = os.path.dirname(os.path.abspath(__file__))

# Concatenate the absolute path and read the .env file.
config = dotenv_values(os.path.join(main_program_path, '.env'))
client = OpenAI(api_key=config["API_KEY"])


def send_request(content, model="gpt-3.5-turbo-1106"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user",
                 "content": f'{command}:\n\n{content}'}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("Error during translation:", e)
        return None

def convert_output_filename(f_name, f_ext):
    f_bilingual = concat_filename_ext(f_name, suffix_bilingual, f_ext)
    f_translated = concat_filename_ext(f_name, suffix_translated, f_ext)
    return f_bilingual, f_translated


def translate_segments(segments):
    open(f'{folder_path}/{f_translated}', 'w').close()
    if output_bilingual:
        open(f'{folder_path}/{f_bilingual}', 'w').close()

    for segment in tqdm(segments, desc="Processing", position=None, leave=True):
        print(f'\n{segment}\n')
        res_translated = send_request(segment)
        if res_translated:
            print(res_translated + '\n')
            with open(f'{folder_path}/{f_translated}', 'a') as f:
                f.write(f'{res_translated}\n')
            if output_bilingual:
                with open(f'{folder_path}/{f_bilingual}', 'a') as f:
                    f.write(f'{segment}\n\n{res_translated}\n\n')


if __name__ == "__main__":
    # read input file name, ext, and path
    inputFile = sys.argv[1]
    file_name, file_extension = os.path.splitext(os.path.basename(inputFile))
    folder_path = os.path.dirname(inputFile)

    # read file
    with open(inputFile, 'r') as f:
        long_text = f.read()

    # Convert output file name.
    f_bilingual, f_translated = convert_output_filename(file_name, file_extension)

    # Split long text.
    segments = split_text_smart(long_text)

    translate_segments(segments)

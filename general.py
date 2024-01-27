import os
import sys
import re
from openai import OpenAI
from dotenv import dotenv_values
import tiktoken
from modules.file_util import concat_filename_ext

model_name = "gpt-3.5-turbo-1106"
encoding_name = "cl100k_base"
suffix = '_output'

# Get absolute path of main program.
main_program_path = os.path.dirname(os.path.abspath(__file__))

# Concatenate the absolute path and read the .env file.
config = dotenv_values(os.path.join(main_program_path, '.env'))
client = OpenAI(api_key=config["API_KEY"])

# Get prompt path.
prompt_path = os.path.join(main_program_path, 'prompt_for_general.txt')


def send_request(content, model="gpt-3.5-turbo-1106"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user",
                 "content": f'{content}'}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("Error during translation:", e)
        return None


def split_text(input_text, max_tokens=4096):
    # 將文字按照換行、空白進行切割
    # re.split(r'\n|\s|。|\.|？|?|！|!', input_text)
    sentences = [sentence.strip() for sentence in re.split(r'\n|\s', input_text) if sentence.strip()]

    # 初始化變數
    # current_chunk_tokens = 0  # 每個chunk的token
    current_chunk = []  # 累積到上限要送出去的sentences
    chunks = []  # 分次送出去的所有chunk
    command_tokens = count_tokens(f'{command}:\n\n', encoding_name)
    current_chunk_tokens = command_tokens

    # 將句子按照模型的 token 上限進行分割
    for i, sentence in enumerate(sentences):
        sentence_tokens = count_tokens(sentence, encoding_name)

        if current_chunk_tokens + sentence_tokens <= max_tokens:
            current_chunk.append(sentence)  # 將sentence塞進chunk
            current_chunk_tokens += sentence_tokens  # 將目前句子token累計至當前chunk的token
            print(f'i: {i}, sentence: {sentence}')
            if sentence == sentences[-1]:
                chunks.append(current_chunk)  # 加入目前chunk至array
        else:
            print(f'sentence in else: {sentence}')
            chunks.append(current_chunk)  # 加入目前chunk至array
            current_chunk = [sentence]  # 將sentence存到新的一個chunk
            current_chunk_tokens = count_tokens(sentence, encoding_name)  # 當前chunk的token為一個句子的token
    return chunks


def count_tokens(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


if __name__ == "__main__":
    # read input file name, ext, and path
    inputFile = sys.argv[1]
    file_name, file_extension = os.path.splitext(os.path.basename(inputFile))
    folder_path = os.path.dirname(inputFile)

    # read file
    with open(inputFile, 'r') as f:
        input_text = f.read()
    with open(prompt_path, 'r') as f:
        command = f.read()

    # Convert output file name.
    f_output = concat_filename_ext(file_name, suffix, file_extension)

    # 切割文字並顯示結果
    chunks = split_text(input_text)

    for chunk in chunks:
        res = send_request(chunk)
        print(res)

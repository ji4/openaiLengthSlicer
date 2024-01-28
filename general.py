import os
import sys
import re
import tiktoken
from openai import OpenAI
from dotenv import dotenv_values
from tqdm import tqdm
from modules.file_util import concat_filename_ext

model_name = "gpt-3.5-turbo-1106"
encoding_name = "cl100k_base"
# max_tokens = 4096
# room_for_punctuation = 500
# max_prompt_tokens = max_tokens - room_for_punctuation
max_tokens = 1000
max_prompt_tokens = 800

suffix = '_output'
command_file_name = 'command_for_general.txt'

# Get absolute path of main program.
main_program_path = os.path.dirname(os.path.abspath(__file__))

# Concatenate the absolute path and read the .env file.
config = dotenv_values(os.path.join(main_program_path, '.env'))
client = OpenAI(api_key=config["API_KEY"])

# Get prompt path.
prompt_path = os.path.join(main_program_path, command_file_name)


def send_request(content, model=model_name):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user",
                 "content": f'{content}'}]
        )
        return response
    except Exception as e:
        print("Error during conversation:", e)
        return None


def add_space_for_two_eng_words(i, sentence, sentences):
    next_index = i+1
    if next_index < len(sentences): # if the next index exists
        if contain_english(sentence) and contain_english(sentences[next_index]):
            sentence += ' '
    return sentence


def split_text(input_text):
    # 將文字按照換行、空白進行切割。
    sentences = [sentence.strip() for sentence in re.split(r'\n|\s', input_text) if sentence.strip()]

    # 初始化變數
    chunks = []
    current_chunk = [command]  # 分次送出去的所有chunk
    current_chunk_tokens = command_tokens

    # 將句子按照模型的 token 上限進行分割
    for i, sentence in enumerate(sentences):
        sentence_tokens = count_tokens(sentence, encoding_name)

        sentence = add_space_for_two_eng_words(i, sentence, sentences)

        if current_chunk_tokens + sentence_tokens <= max_prompt_tokens:
            current_chunk.append(sentence)  # 將sentence塞進chunk
            current_chunk_tokens += sentence_tokens  # 將目前句子token累計至當前chunk的token
            if sentence == sentences[-1]:
                chunks.append(current_chunk)  # 加入目前chunk至array
        else:
            print(f'sentence in else: {sentence}')
            chunks.append(current_chunk)
            # Empty current chunk for new storage.
            current_chunk = [command, sentence]

            # 當前chunk的token為command + 一個句子的token
            current_chunk_tokens = command_tokens + count_tokens(sentence, encoding_name)
    return chunks


def count_tokens(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def calculate_used_tokens(total_tokens, prompt_tokens, completion_tokens):
    total_tokens += total_tokens
    prompt_tokens += prompt_tokens
    completion_tokens += completion_tokens
    return total_tokens, prompt_tokens, completion_tokens


def convert_prompt(chunks):
    open(output_file_path, 'w').close()

    for chunk in tqdm(chunks, desc="Processing", position=-1, leave=True):
        print(f'\nProcessing paragraph:\n{" ".join(chunk).replace(command, "")}')

        text_tokens = count_tokens(''.join(chunk).replace(command, ''), encoding_name)
        print(
            f'Request of the current paragraph (contains command, {command_tokens} tokens): {command_tokens + text_tokens} tokens.')
        # Init tokens used.
        total_tokens = prompt_tokens = completion_tokens = 0

        res = send_request(''.join(chunk))
        if res:
            total_tokens, prompt_tokens, completion_tokens = calculate_used_tokens(res.usage.total_tokens,
                                                                                   res.usage.prompt_tokens,
                                                                                   res.usage.completion_tokens)
            res_content = res.choices[0].message.content

            print(f'Response of the current paragraph: {completion_tokens} tokens.')
            print(f'Converted: {res_content}\n')

            with open(output_file_path, 'a') as f:
                f.write(f'{res_content}\n\n')

    print(f'Total tokens: {total_tokens}, Prompt Tokens: {prompt_tokens}, Completion Tokens: {completion_tokens}')


def contain_english(text):
    return bool(re.search('[a-zA-Z]', text))


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
    output_file_path = f'{folder_path}/{f_output}'  # output path

    # Count command tokens
    command += ':\n\n'
    command_tokens = count_tokens(command, encoding_name)

    # 切割文字
    chunks = split_text(input_text)
    # print(f'chunks: {chunks}')

    # Convert prompt
    convert_prompt(chunks)

import os
import sys
import re
import tiktoken
import shutil
from openai import OpenAI, OpenAIError
from dotenv import dotenv_values
from tqdm import tqdm
from modules.file_util import concat_filename_ext
from modules.token_usage import Token
from modules.color import Color

model_name = "gpt-3.5-turbo-1106"
encoding_name = "cl100k_base"
system_content = 'You are a professional stenographer.'

# max_tokens = 4096
# room_for_punctuation = 300
# max_prompt_tokens = max_tokens/2 - room_for_punctuation

#For Test
max_tokens = 200
max_prompt_tokens = max_tokens * 0.6

suffix = '_output'
command_file_name = 'command_for_punctuationize.txt'

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
                {"role": "system",
                 "content": f'{system_content}'},
                {"role": "user",
                 "content": f'{content}'}
            ]
        )
        return response
    except Exception as e:
        tqdm.write("Error during conversation:", e)
        return None


def add_space_for_two_eng_words(i, cur_sentence, sentences):
    next_index = i + 1
    if contain_english(cur_sentence) and next_index < len(sentences):  # if the next index exists
        if contain_english(sentences[next_index]):
            cur_sentence += ' '
    return cur_sentence


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
            if sentence == sentences[-1]:  # 只有一個chunk
                chunks.append(current_chunk)  # 加入目前chunk至array
        else:
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


def write_res_to_file(res, cur_chunk_tokens):
    if res:
        res_content = res.choices[0].message.content
        cur_chunk_tokens.completion_tokens = res.usage.completion_tokens
        cur_chunk_tokens.total_tokens = res.usage.total_tokens
        cur_chunk_tokens.prompt_tokens = res.usage.prompt_tokens

        tqdm.write(f'Actual Request of the current paragraph: {cur_chunk_tokens.prompt_tokens} tokens.')
        print_full_line('.')
        tqdm.write(f'{Color.BG_GREY}{Color.BLACK}[Response of the of paragraph]{Color.RESET}\n'
                   f'{cur_chunk_tokens.completion_tokens} tokens.')
        tqdm.write(f'{Color.BG_BLACK}Converted: {Color.GREEN}{res_content}{Color.RESET}')
        print_full_line('.')

        with open(output_file_path, 'a') as f:
            f.write(f'{res_content}\n\n')
        return cur_chunk_tokens


def init_cur_chunk_token_usage(chunk):
    cur_chunk_tokens = Token()
    cur_chunk_tokens.text_tokens = count_tokens(''.join(chunk).replace(command, ''), encoding_name)
    cur_chunk_tokens.command_tokens = command_tokens
    cur_chunk_tokens.prompt_tokens = command_tokens + count_tokens(system_content, encoding_name) + cur_chunk_tokens.text_tokens

    return cur_chunk_tokens

def convert_prompt(chunks):
    open(output_file_path, 'w').close()
    sum_chunks_tokens = Token()

    print_full_line('=')

    try:
        for chunk in tqdm(chunks, desc="Processing"):
            cur_chunk_tokens = init_cur_chunk_token_usage(chunk)
            tqdm.write(
                f'\n{Color.BG_GREY}{Color.BLACK}[Request of the current paragraph]{Color.RESET}\n'
                f'prompt (roughly estimated): {cur_chunk_tokens.prompt_tokens} tokens\n(command: {cur_chunk_tokens.command_tokens} tokens , text: {cur_chunk_tokens.text_tokens} tokens, others: {cur_chunk_tokens.prompt_tokens - cur_chunk_tokens.command_tokens - cur_chunk_tokens.text_tokens} tokens.\n')
            tqdm.write(f'Processing paragraph: {Color.BG_BLACK}{Color.YELLOW}{" ".join(chunk).replace(command, "")}{Color.RESET}')

            res = send_request(''.join(chunk))
            cur_chunk_tokens = write_res_to_file(res, cur_chunk_tokens)
            sum_chunks_tokens.add_sum(cur_chunk_tokens)

            tqdm.write(f'{Color.BG_GREY}{Color.BLACK}[Accumulated Usage So Far]{Color.RESET}')
            sum_chunks_tokens.print_token_usage()
            sum_chunks_tokens.print_cost()
            tqdm.write('\n')
            print_full_line('=')
    except OpenAIError as e:
        tqdm.write("OpenAI Error:", e)
    except IOError as e:
        tqdm.write("IO Error:", e)
    except Exception as e:
        tqdm.write("Unexpected error:", e)
    else:
        tqdm.write("Conversion completed successfully!\n")
    finally:
        print_full_line('=')
        tqdm.write(f'{Color.BG_GREY}{Color.BLACK}[Sum Usage]{Color.RESET}')

        sum_chunks_tokens.print_token_usage()
        sum_chunks_tokens.print_cost()
        print_full_line('=')
        tqdm.write(f'{Color.BG_GREY}{Color.BLACK}Output file:{Color.RESET} {output_file_path}')
        print_full_line('=')


def contain_english(text):
    return bool(re.search('[a-zA-Z]', text))

def print_full_line(str_character):
    # 获取终端的宽度
    terminal_width, _ = shutil.get_terminal_size()

    # 使用 ANSI 转义码输出水平线
    tqdm.write(str_character * terminal_width)


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

    # Convert prompt
    convert_prompt(chunks)

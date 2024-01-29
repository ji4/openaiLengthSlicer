# Requirements
```
pip install tqdm
pip install python-dotenv
pip install tiktoken
```
# Configuration
## Steps
1. Open the `.env` file in the project's root directory. (Tip for Mac OSX users: Press `Command`+`Shift`+`.` in Finder to show hidden files.)
2. Paste your API Key after `API_KEY=` and replace `your_api_key_here`.
4. Save and close the file.

## Optional
* Edit command of prompt in `command_for_punctuationize.txt`.

# Usage
* For **translator.py**:

    `python3 translate.py <file_path>`


* For **puntuactionize.py**:

    `python3 punctuationize.py <file_path>`

# Logic of Flow (punctuationize.py)
![Flow.jpg](images%2FFlow.jpg)

# Known Issues 
**puctuationize.py**
### Issue: Extra Content Added in Response (Sometimes)
There is no use to add `無需添加其他任何文字` in the `command_for_punctuationize.txt` file.
 ![Extra Content Added in Response.png](images%2FExtra%20Content%20Added%20in%20Response.png)
### Issue: No Appropriate Break Line in A Long Paragraph After Converted
The following image is a converted file.
There's no use to add `並適當換行` in the `command_for_punctuationize.txt` file.
![No Appropriate Break Line in A Long Paragraph.png](images%2FNo%20Appropriate%20Break%20Line%20in%20A%20Long%20Paragraph.png)
### Issue: Sometimes OpenAI Shows That It Cannot Finish My Request
Sometimes the expected output of a converted paragraph is responded as 「很抱歉，我無法完成你的請求。」 or something like that.

The same original input text might be successfully converted or fail each time the program is executed.

![Sometimes A Paragraph is Converted While Sometimes Not.png](images%2FSometimes%20A%20Paragraph%20is%20Converted%20While%20Sometimes%20Not.png)

Here's the response of failed message:
```
ChatCompletion(
  (id = 'chatcmpl-8mDCEmlXfAiS9cPzyv7GxLIWBXDG2'),
  (choices = [
    Choice(
      (finish_reason = 'stop'),
      (index = 0),
      (logprobs = None),
      (message = ChatCompletionMessage(
        (content = '抱歉，我無法更改您所提供的文字。'),
        (role = 'assistant'),
        (function_call = None),
        (tool_calls = None),
      )),
    ),
  ]),
  (created = 1706501162),
  (model = 'gpt-3.5-turbo-1106'),
  (object = 'chat.completion'),
  (system_fingerprint = 'fp_b57c83dd65'),
  (usage = CompletionUsage(
    (completion_tokens = 17),
    (prompt_tokens = 1763),
    (total_tokens = 1780),
  )),
);
```
### Sometimes OpenAI Echos My Question
![Sometimes OpenAI Echos My Question.png](images%2FSometimes%20OpenAI%20Echos%20My%20Question.png)

### Issue: Actual Tokens of Request is Not Accurately Estimated
Before sending the request, the tokens calculated is the same as the actual response.
![Actual Tokens of Request is Not Accurately Estimated.png](images%2FActual%20Tokens%20of%20Request%20is%20Not%20Accurately%20Estimated.png)
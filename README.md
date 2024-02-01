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
Current version (v1.1.0)
![Flow_v1_1_0.jpg](images%2FFlow_v1_1_0.jpg)

# Known Issues 
The following issues come out occasionally, not all the time.  
**punctuationize.py**
### Issue: Extra Content Added in Response (Sometimes)
There is no use to add `無需添加其他任何文字` in the `command_for_punctuationize.txt` file.
 ![Extra Content Added in Response.png](images%2FExtra%20Content%20Added%20in%20Response.png)

### Issue: Sometimes OpenAI Shows That It Cannot Finish My Request
Sometimes the expected output of a converted paragraph is responded as 「很抱歉，我無法完成你的請求。」 or something like that.

The same original input text might be successfully converted or fail each time the program is executed.

![Sometimes A Paragraph is Converted While Sometimes Not.png](images%2FSometimes%20A%20Paragraph%20is%20Converted%20While%20Sometimes%20Not.png)

Here's the response of failed message, and it shows that my token usage didn't exceed the limit.
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
I revised my prompt to ask it to explain complete failed reason, but sometimes still got simple response.
![No More Explained.png](images%2FNo%20More%20Explained.png)

### Issue: Sometimes OpenAI Echos My Question
![Sometimes OpenAI Echos My Question.png](images%2FSometimes%20OpenAI%20Echos%20My%20Question.png)
There is no use to ask it not to echo in the command.
![Sometimes OpenAI Echos My Question 2.png](images%2FSometimes%20OpenAI%20Echos%20My%20Question%202.png)

### Issue: Actual Tokens of Request is Not Accurately Estimated
Before sending the request, the tokens calculated is not the same as the actual response.
![Actual Tokens of Request is Not Accurately Estimated.png](images%2FActual%20Tokens%20of%20Request%20is%20Not%20Accurately%20Estimated.png)

### Issue: In The Old Version (v1.0.0), It Sometimes Says It Cannot Complete My Request Due To Unclear Break. 
#### Differences in Test Versions

**v1.0.0 (old version)**

In the previous version, I removed all the spaces between sentences to save tokens sent in the request.
![Flow_v1_0_0.jpg](images%2FFlow_v1_0_0.jpg)

Sometimes I got the following responses according to the above flow:
![Failure 4.png](images%2FFailure%204.png)
To fix this, I revised it as the following version, which spaces will be sent via request. And that cost more tokens.

**v1.1.0 (current version)**
![Flow_v1_1_0_revised.jpg](images%2FFlow_v1_1_0_revised.jpg)

Sometimes it still responses that the context are not coherent sentences.
![Failure 11.png](images%2FFailure%2011.png)

### Issue: Possible Failure of Responses 🙄
![Failure 1.png](images%2FFailure%201.png)
![Failure 2.png](images%2FFailure%202.png)
![Failure 3.png](images%2FFailure%203.png)
![Failure 5.png](images%2FFailure%205.png)
![Failure 6.png](images%2FFailure%206.png)
![Failure 7.png](images%2FFailure%207.png)
![Failure 8.png](images%2FFailure%208.png)
![Failure 9.png](images%2FFailure%209.png)
* Sometimes Simplified Chinese Still Comes Out Even I Command It Response In Traditional Chinese Or zh-tw  
![Command Of Traditional Chinese.png](images%2FCommand%20Of%20Traditional%20Chinese.png)
![Failure 10 - Simplied Chinese.png](images%2FFailure%2010%20-%20Simplied%20Chinese.png)

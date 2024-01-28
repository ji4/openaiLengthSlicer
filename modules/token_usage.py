class Token:
    def __init__(self):
        self.total_tokens = 0
        self.prompt_tokens = 0
        self.completion_tokens = 0

        # prompt_tokens = command_tokens + text_tokens
        self.command_tokens = 0
        self.text_tokens = 0

    def add_sum(self, token):
        self.total_tokens += token.total_tokens
        self.prompt_tokens += token.prompt_tokens
        self.completion_tokens += token.completion_tokens

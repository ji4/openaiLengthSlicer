from tqdm import tqdm

class Token:
    def __init__(self):
        self.total_tokens = 0
        self.prompt_tokens = 0
        self.completion_tokens = 0

        # prompt_tokens = command_tokens + text_tokens
        self.command_tokens = 0
        self.text_tokens = 0

        # charge cost
        self.unit_of_tokens_charged = 1000
        self.prompt_price = 0.0001
        self.completion_price = 0.0002
        self.exchange_rate_of_US_to_NT = 30
        self.ndigits = 5

    def add_sum(self, token):
        self.total_tokens += token.total_tokens
        self.prompt_tokens += token.prompt_tokens
        self.completion_tokens += token.completion_tokens

    def print_cost(self):
        prompt_cost = self.prompt_tokens / self.unit_of_tokens_charged * self.prompt_price * self.exchange_rate_of_US_to_NT
        completion_cost = self.completion_tokens / self.unit_of_tokens_charged * self.completion_price * self.exchange_rate_of_US_to_NT
        total_cost = prompt_cost + completion_cost

        tqdm.write(
            f'Total Cost: ${round(total_cost, self.ndigits)}, '
            f'Prompt Cost: ${round(prompt_cost, self.ndigits)}, '
            f'Completion Cost: ${round(completion_cost, self.ndigits)} '
            f'NT dollars (USD:TWD=1:30)')

import os
from openai import AzureOpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam


def prompt():
    client = AzureOpenAI(
        api_key=os.environ["API_KEY"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_version=os.environ["API_VERSION"],
    )

    response = client.chat.completions.create(
        model=os.environ["MODEL"], # This does not need to be an environment variable
        # messages=[
        #     {"role": "system", "content": "You are a helpful assistant."},
        #     {"role": "user", "content": "Does Azure OpenAI support customer managed keys?",},
        #     {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI.",},
        #     {"role": "user", "content": "Do other Azure AI services support this too?"},
        # ],
        # Amandoua optiuniile sunt valide numa ca la prima comenteaza ca nu folosesti clasele lor
        # si la adoua comenteaza ca nu ii pui role="system" care de fapt ii singura optiune care merge
        messages=[
            ChatCompletionSystemMessageParam(content="You are a helpful assistant."),
            ChatCompletionUserMessageParam(content="Give me a two-line Python tip."),
        ],
        # max_tokens=100, # Unsupported with this model use max_completion_tokens instead
        # max_completion_tokens=100,

        # [0-2] Controls randomness
        # Lower values more deterministic
        # Higher values more randomness more prone to hallucinate
        # temperature=0.7,
    )

    print(response.to_json())

if __name__ == "__main__":
    # prompt()
    print(os.environ["API_KEY"])
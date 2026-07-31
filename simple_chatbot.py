import os
from dotenv import load_dotenv
from openai import OpenAI


def main():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment. Please create a .env file.")
        return

    client = OpenAI(api_key=api_key)

    print("Simple OpenAI Chatbot")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "exit":
            print("Goodbye!")
            break

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input},
                ],
                max_tokens=150,
            )
            assistant_message = response.choices[0].message.content.strip()
            print(f"Bot: {assistant_message}")
        except Exception as err:
            print(f"Error: {err}")


if __name__ == "__main__":
    main()

from openai import OpenAI
import os


def main():
    client = OpenAI(
    organization=os.getenv('OPENAI_ORGANIZATION_ID'),
    project=os.getenv('OPENAI_PROJECT_ID'),
    )

    messages=[
        {"role": "system", "content": "You are a customer support chat from Imetiato Nautica a online e-comerce store for marine products. You only answer product related questions."},
        {"role": "user", "content": "What is the name of te lines used to raise the main sail?"},
        {"role": "assistant", "content": "The line used to raise the main sail is called main halyard. You can find it for sale in or online store. Thank you for choosing the Imediato Nautica."},
        ]

    # Set up a continuous loop to chat
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Exiting chat...")
            break

        messages.append({"role": "user", "content": user_input}),
        try:
            # Call the OpenAI API with your input using the gpt-3.5-turbo model
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                stream=True,
            )

            # Print out the model's response
            response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    response += chunk.choices[0].delta.content
            print("AI: ", response)
            messages.append({"role": "assistant", "content": response}),
            

        except Exception as e:
            print("An error occurred:", e)

if __name__ == "__main__":
    main()



import openai

# Set your OpenAI API key
openai.api_key = "6d0bb850baca4243160e585f3f4bfd31b3a74392d1251f6d98f51d8870c0fb57"

def ask_llama(question):
    try:
        # Make a request to the OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use the appropriate model
            prompt=question,
            max_tokens=150,
            temperature=0.7
        )
        # Extract and return the response text
        return response.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    # Ask the user for a question
    user_question = input("What would you like to ask Llama? ")
    # Get the response from the API
    answer = ask_llama(user_question)
    # Print the response
    print("Llama's response:", answer)
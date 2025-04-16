import google.generativeai as genai

genai.configure(api_key="AIzaSyBrkhg_PdODk0zr6V5klE09bMJQPJoHQCI")
for m in genai.list_models():
    print(m.name)

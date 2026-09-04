from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

model = OllamaLLM(model="llama3.2")

template = """

You are an expert in answering inquiries about a pizza restaurant.
Only use information present in the reviews below. If the reviews
don't contain the answer, say so clearly instead of guessing.

Here are some relevant reviews: {reviews}

Here is the question to answer: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


while True:
    print("\n\n-------------------------------------")
    question = input("Provide your inquiry (type q to quit ): ")
    print("\n\n")
    if question == "q":
        break



    reviews = retriever.invoke(question)
    result = chain.invoke({"reviews": reviews, "question": question})
    print("\nAnswer:")
    print(result)
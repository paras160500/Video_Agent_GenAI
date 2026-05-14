from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough , RunnableLambda
import os 

def get_llm():
    return ChatMistralAI(model='mistral-small-latest' , mistral_api_key = os.getenv('MISTRAL_API_KEY') , temperature=0.2)

def build_chain(system_prompt : str):
    llm = get_llm()
    return (
        RunnablePassthrough() | RunnableLambda(lambda x : {'text' : x}) | ChatPromptTemplate.from_messages(
            [
                ('system' , system_prompt),
                ('human' , '{text}')
            ]
        ) | llm | StrOutputParser()
    )

def extract_action_items(transcript : str) -> str:
    chain = build_chain(
        """You are an expert metting analyst. From the metting transcript,
        extract all action items. for each provide:\n
        - Task description\n
        - Owner (who is responsible) \n
        - Deadline (if mentioned, else write 'Not Specified')\n\n
        Format as a numbered list. In none found say 'No action items found."""
    )

    return chain.invoke(transcript)

def extract_key_decisions(transcript : str) -> str:
    chain = build_chain("""You are an expert meeting analyst.From the metting transcript,
                        extract all key decision made.Format as a numbered list.
                        If none. founc say 'No key decision found.""")
    return chain.invoke(transcript)

def extract_questions(transcript : str) -> str:
    chain = build_chain("""From the meeting transcript, extract all unresolved questions or
                        topics needing follow-up. Format. as. a numbered list.
                        If none found say 'No open question found.""")
    return chain.invoke(transcript)

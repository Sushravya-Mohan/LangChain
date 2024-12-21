import validators
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader


# Streamlit app
st.set_page_config(
    page_title="LangChain: Summarize Text from YT or Website", page_icon="🦜"
)
st.title("🦜 LangChain: Summarize Text from YT or Website")
st.subheader("Summarize URL")

# Get the Groq API key and url to be summarized
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", value="", type="password")

generic_url = st.text_input("URL", label_visibility="collapsed")

prompt_template = """
Provide a summary of the following content in 300 words:
Content: {text}
"""

prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

if st.button("Summarize the content from YT or Website"):
    # Validate all the inputs
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide the information to get started.")
    elif not validators.url(generic_url):
        st.error("Please enter a valid URL. It may be a YT video or website URL.")

    else:
        # Gemma model using Groq API
        llm = ChatGroq(groq_api_key=groq_api_key, model="gemma2-9b-it")
        try:
            with st.spinner("Waiting......."):
                # Loading the website or YT video
                if "youtube.com" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(
                        generic_url, add_video_info=True
                    )
                else:
                    loader = UnstructuredURLLoader(
                        urls=[generic_url],
                        ssl_verify=False,
                        headers={
                            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
                        },
                    )

                docs = loader.load()
                print(docs)

                # Chain for summarization
                chain = load_summarize_chain(llm=llm, chain_type="stuff", prompt=prompt)
                output_summary = chain.run(docs)

                st.success(output_summary)
        except Exception as e:
            st.exception(f"Exception: {e}")

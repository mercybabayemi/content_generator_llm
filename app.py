import streamlit as st
from datetime import datetime

from fast_api.apis import generate_endpoint
from llm_client.generate import generate

st.set_page_config(page_title="ENUMVERSE Course Content Generator", layout="wide")

# ---- Session state for chat history ----
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi 👋 What do you have in mind? Ask me anything, and I will generate any learning curriculum and course content you need."
        }
    ]

# Detect if user has sent at least one message
has_user_message = any(m.get("role") == "user" for m in st.session_state.messages)

# ---- CSS: center first, then stick to bottom after first user message ----
if has_user_message:
    # After first user message: pin input to bottom
    st.markdown(
        """
        <style>
          .block-container { padding-bottom: 6rem; }

          div[data-testid="stChatInput"] {
            position: fixed;
            bottom: 1.25rem;
            left: 50%;
            transform: translateX(-50%);
            width: min(980px, calc(100% - 2rem));
            z-index: 999;
          }

          div[data-testid="stChatInput"] > div {
            background: rgba(0,0,0,0.35);
            backdrop-filter: blur(8px);
            border-radius: 14px;
            padding: 0.25rem 0.25rem;
            border: 1px solid rgba(255,255,255,0.08);
          }

          div[data-testid="stChatMessage"] { padding-top: 0.25rem; padding-bottom: 0.25rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    # Before any user message: keep input in normal flow and visually center it
    # (No fixed positioning)
    st.markdown(
        """
        <style>
          /* Create vertical breathing room so the input appears near the middle */
          .block-container { padding-top: 18vh; padding-bottom: 2rem; }

          /* Ensure chat input is NOT fixed before first message */
          div[data-testid="stChatInput"] {
            position: static !important;
            width: min(980px, calc(100% - 2rem));
            margin: 0 auto;
            transform: none !important;
          }

          div[data-testid="stChatInput"] > div {
            background: rgba(0,0,0,0.20);
            backdrop-filter: blur(6px);
            border-radius: 14px;
            padding: 0.25rem 0.25rem;
            border: 1px solid rgba(255,255,255,0.08);
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

st.title("Learning Content Generator")

# ---- Render chat history ----
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---- Chat input ----
prompt = st.chat_input("Ask anything in mind...")

def mock_generate_reply(user_text: str) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return (
        f"**Got it.** Here’s a draft response to:\n\n"
        f"> {user_text}\n\n"
        f"**(Placeholder output — connect your model next.)**\n\n"
        f"- Timestamp: {now}\n"
        #f"- Next step: replace `mock_generate_reply()` with your API/model call."
    )

if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Generating..."):
            # reply = mock_generate_reply(prompt)
            reply = generate(prompt)
            st.markdown(reply)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # Force rerun so the CSS switches immediately to "sticky bottom" mode
    st.rerun()

# Optional: clear chat button
with st.sidebar:
    st.subheader("Chat controls")
    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Chat cleared ✅ Ask anything in mind."
            }
        ]
        st.rerun()

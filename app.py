import os
import time

import streamlit as st
from PIL import Image

from strands import Agent
from strands.models.gemini import GeminiModel


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Circuit Doctor",
    page_icon="🔧",
    layout="wide",
)


# =========================================================
# SIMPLE DARK THEME
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 10% 0%,
                rgba(59, 130, 246, 0.12),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 0%,
                rgba(20, 184, 166, 0.08),
                transparent 28%
            ),
            #07111d;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# API KEY
# =========================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# =========================================================
# HEADER
# =========================================================

left_header, right_header = st.columns(
    [5, 1],
    gap="large"
)

with left_header:

    st.title("🔧 Circuit Doctor")

    st.caption(
        "AI-powered Arduino & breadboard troubleshooting"
    )


with right_header:

    st.success("🟢 Ready")


st.divider()


# =========================================================
# HERO
# =========================================================

hero_left, hero_right = st.columns(
    [1.2, 0.8],
    gap="large"
)


with hero_left:

    st.markdown(
        "### ⚡ Your circuit's second pair of eyes"
    )

    st.markdown(
        "# Fix Smarter. Build Confidently."
    )

    st.write(
        "Your LED isn't lighting up? "
        "A jumper wire looks suspicious?"
    )

    st.markdown(
        "**Take a photo and let's figure it out.**"
    )

    st.write(
        "Circuit Doctor looks at the visible parts "
        "and connections in your circuit and helps "
        "you figure out what to check next."
    )

    st.caption(
        'Built for those "Why isn\'t this working?" moments.'
    )


with hero_right:

    with st.container(border=True):

        st.markdown(
            "### 👀 What Circuit Doctor does"
        )

        st.write(
            "Upload one clear photo of your circuit. "
            "The AI examines what it can actually see "
            "and gives you practical troubleshooting guidance."
        )

        st.write("")

        st.info(
            "🧠 AI Vision\n\n"
            "🔌 Circuit Analysis\n\n"
            "🛠️ Troubleshooting Guidance"
        )


# =========================================================
# HOW IT HELPS
# =========================================================

st.divider()

st.markdown(
    "## What can I help you with?"
)

st.caption(
    "No complicated setup. Just show Circuit Doctor what you built."
)


card1, card2, card3 = st.columns(
    3,
    gap="medium"
)


with card1:

    with st.container(border=True):

        st.markdown(
            "### 📷 Show your circuit"
        )

        st.write(
            "Take a clear photo of your Arduino "
            "or breadboard and upload it."
        )


with card2:

    with st.container(border=True):

        st.markdown(
            "### 🧠 Let AI take a look"
        )

        st.write(
            "Circuit Doctor checks the visible "
            "components, wires and connections."
        )


with card3:

    with st.container(border=True):

        st.markdown(
            "### 🛠️ Know what to check"
        )

        st.write(
            "Get practical next steps instead of "
            "guessing which wire might be wrong."
        )


# =========================================================
# UPLOAD SECTION
# =========================================================

st.divider()

st.markdown(
    "## 📸 Show me what you're building"
)

st.caption(
    "Nothing is preloaded. Upload a circuit photo to begin."
)


uploaded_file = st.file_uploader(
    "Choose your circuit image",
    type=[
        "png",
        "jpg",
        "jpeg"
    ],
)


# =========================================================
# EMPTY STATE
# =========================================================

if uploaded_file is None:

    with st.container(border=True):

        st.markdown(
            "### 📷 Your circuit goes here"
        )

        st.write(
            "Choose a PNG or JPG photo of your "
            "Arduino or breadboard."
        )

        st.info(
            "💡 Tip: Take the photo from above and keep "
            "the Arduino pins, breadboard rows, LED and "
            "jumper wires visible."
        )


# =========================================================
# IMAGE UPLOADED
# =========================================================

if uploaded_file is not None:

    image = Image.open(
        uploaded_file
    )

    image_bytes = uploaded_file.getvalue()

    image_format = (
        uploaded_file.type.split("/")[-1]
        if uploaded_file.type
        else "png"
    )


    st.divider()


    image_col, analysis_col = st.columns(
        [1, 1],
        gap="large"
    )


    # =====================================================
    # CIRCUIT IMAGE
    # =====================================================

    with image_col:

        st.markdown(
            "### 📷 Your circuit"
        )

        with st.container(border=True):

            st.image(
                image,
                width="stretch"
            )

        st.caption(
            "This is the photo Circuit Doctor will inspect."
        )


    # =====================================================
    # ANALYSIS PANEL
    # =====================================================

    with analysis_col:

        st.markdown(
            "### 🩺 Circuit Doctor"
        )

        with st.container(border=True):

            st.success(
                "✅ Photo received"
            )

            st.write(
                "I've got the photo. "
                "Let's take a closer look at what's visible."
            )

            st.write("")

            analyze_button = st.button(
                "🔬 Analyze My Circuit",
                type="primary",
                width="stretch"
            )


        # =================================================
        # RUN AI
        # =================================================

        if analyze_button:

            if not GEMINI_API_KEY:

                st.error(
                    "Gemini API key not found."
                )

                st.code(
                    "set GEMINI_API_KEY=YOUR_API_KEY",
                    language="cmd"
                )

                st.stop()


            # =================================================
            # PROMPT
            # =================================================

            prompt = """
You are Circuit Doctor, a friendly electronics
lab assistant helping a student troubleshoot
an Arduino or breadboard circuit.

Carefully inspect the uploaded photograph.

Your job is to distinguish between:

1. What is clearly visible.
2. What looks possible but cannot be confirmed.
3. What the student should check next.

IMPORTANT:

Only state things that are visually supported
by the photograph.

DO NOT:

- invent components
- invent Arduino pin numbers
- invent resistor values
- invent hidden wires
- assume hidden electrical connections
- claim a definite fault without visual evidence

If something cannot be determined from the image,
write:

"Cannot verify from image."

Look for:

- Arduino board
- breadboard
- LED
- resistor
- jumper wires
- sensors
- modules
- visible power connections
- visible ground connections
- visible Arduino connections
- visible breadboard connections
- LED orientation if visible
- obvious wiring problems
- possible short circuits
- obvious missing connections


Return the result using exactly these sections:


## 🔌 Components

List the components that are clearly visible.


## 🔗 Visible Connections

Describe only the connections that can actually
be seen.


## ⚠️ Possible Issues

List possible problems supported by visible evidence.

For each problem, briefly explain what you can
see that makes it worth checking.

If no obvious problem can be confirmed, write:

"No obvious issue can be confirmed from this image."


## 👀 What I Cannot Verify

Mention anything hidden or unclear, including:

- Arduino pin numbers
- resistor values
- hidden wires
- obscured connections
- component details


## 🛠️ What To Check Next

Give 3–5 simple troubleshooting steps.

Put the easiest checks first.


## 📊 Confidence

Choose one:

Low
Moderate
High

Then briefly explain why.


STYLE:

Speak like a helpful electronics lab partner.

Keep the explanation simple.

Avoid unnecessary jargon.

Never pretend to know something
the photograph does not show.
"""


            # =================================================
            # CREATE MODEL
            # =================================================

            model = GeminiModel(
                client_args={
                    "api_key": GEMINI_API_KEY
                },

                model_id="gemini-3.6-flash",

                params={
                    "max_output_tokens": 1600
                }
            )


            agent = Agent(
                model=model
            )


            # =================================================
            # CALL GEMINI WITH RETRY
            # =================================================

            response = None

            last_error = None


            with st.spinner(
                "🔍 Looking closely at your circuit..."
            ):

                for attempt in range(3):

                    try:

                        response = agent(
                            [
                                {
                                    "role": "user",

                                    "content": [

                                        {
                                            "text": prompt
                                        },

                                        {
                                            "image": {

                                                "format": image_format,

                                                "source": {
                                                    "bytes": image_bytes
                                                }

                                            }
                                        }

                                    ]
                                }
                            ]
                        )

                        break


                    except Exception as error:

                        last_error = error

                        error_text = (
                            str(error)
                            .lower()
                        )

                        temporary_error = (
                            "503" in error_text
                            or
                            "service unavailable"
                            in error_text
                            or
                            "temporarily unavailable"
                            in error_text
                            or
                            "high demand"
                            in error_text
                        )


                        if (
                            temporary_error
                            and
                            attempt < 2
                        ):

                            time.sleep(
                                2 + attempt * 2
                            )

                            continue


                        break


            # =================================================
            # DISPLAY RESULT
            # =================================================

            if response is not None:

                result_text = str(
                    response
                ).strip()


                if not result_text:

                    result_text = (
                        "The AI returned an empty response. "
                        "Please try again."
                    )


                st.success(
                    "✅ Diagnosis complete"
                )


                st.markdown(
                    "## 🩺 Here's what I noticed"
                )

                st.caption(
                    "Based only on what can be seen in your photo."
                )


                result_image, result_text_col = st.columns(
                    [0.85, 1.15],
                    gap="large"
                )


                with result_image:

                    with st.container(border=True):

                        st.image(
                            image_bytes,
                            width="stretch"
                        )


                    st.caption(
                        "Circuit reviewed"
                    )


                with result_text_col:

                    with st.container(border=True):

                        st.markdown(
                            result_text
                        )


                st.warning(
                    "⚠️ Always verify physical connections "
                    "before powering the circuit."
                )


            # =================================================
            # ERROR
            # =================================================

            else:

                st.error(
                    "I couldn't complete the analysis right now."
                )


                if last_error is not None:

                    error_text = (
                        str(last_error)
                        .lower()
                    )


                    if (
                        "503" in error_text
                        or
                        "service unavailable"
                        in error_text
                        or
                        "temporarily unavailable"
                        in error_text
                        or
                        "high demand"
                        in error_text
                    ):

                        st.info(
                            "Gemini is temporarily busy. "
                            "Wait a few seconds and click "
                            "\"Analyze My Circuit\" again."
                        )

                    else:

                        st.info(
                            "Please check your Gemini API key "
                            "and internet connection."
                        )


                    with st.expander(
                        "Technical details"
                    ):

                        st.code(
                            str(last_error)
                        )


# =========================================================
# HUMAN TOUCH
# =========================================================

st.divider()

st.markdown(
    "## 🔧 Built for the frustrating lab moments"
)

with st.container(border=True):

    st.markdown(
        '### "Why isn\'t this working?"'
    )

    st.write(
        "You don't need to know exactly what's wrong "
        "before asking for help. Show Circuit Doctor "
        "what you've built, start with the easiest checks, "
        "and learn while you fix it."
    )


# =========================================================
# HOW IT WORKS
# =========================================================

st.divider()

st.markdown(
    "## ⚙️ How it works"
)

st.caption(
    "Three simple steps."
)


s1, s2, s3 = st.columns(
    3,
    gap="medium"
)


with s1:

    with st.container(border=True):

        st.markdown(
            "### ① Upload"
        )

        st.write(
            "Take a clear photo of your circuit."
        )


with s2:

    with st.container(border=True):

        st.markdown(
            "### ② AI takes a look"
        )

        st.write(
            "Circuit Doctor examines the visible "
            "components and connections."
        )


with s3:

    with st.container(border=True):

        st.markdown(
            "### ③ Figure out the next step"
        )

        st.write(
            "Get practical things to check before "
            "you start changing everything."
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🔧 Circuit Doctor • Built with AWS Strands Agents + Gemini"
)

st.caption(
    "AI-assisted diagnosis — always verify connections "
    "before powering your circuit."
)
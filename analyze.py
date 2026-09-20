import boto3

IMAGE_PATH = "circuit.png"
MODEL_ID = "amazon.nova-lite-v1:0"

client = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1"
)

with open(IMAGE_PATH, "rb") as f:
    image_bytes = f.read()

prompt = """
You are Circuit Doctor, an AI electronics troubleshooting assistant.

Analyze ONLY what can be visually verified from the image.

Your job is to:

1. Identify visible electronic components.
2. Trace visible connections between the Arduino, breadboard, wires, LED and resistors as far as the image allows.
3. Look for obvious wiring mistakes, incorrect component placement, reversed LED polarity, missing connections, or short circuits.
4. Do NOT assume that a component is faulty or disconnected unless there is visual evidence.
5. Do NOT mention generic possibilities just to fill the answer.
6. If a connection cannot be verified because wires or breadboard rows are hidden, explicitly say "Cannot verify from image."
7. Clearly distinguish between CONFIRMED issues and POSSIBLE issues.
8. Never claim that the USB cable is faulty merely because it is visible.
9. Do not invent resistor colors, values, or connections that cannot be clearly seen.

Return exactly this format:

COMPONENTS:
- Component — confidence

CONFIRMED CONNECTIONS:
- ...

POSSIBLE ISSUES:
- Issue — evidence — confidence
- If none can be confirmed, say "No obvious issue can be confirmed from this image."

WHAT CANNOT BE VERIFIED:
- ...

TROUBLESHOOTING:
1. ...
2. ...
3. ...

OVERALL CONFIDENCE:
Low / Moderate / High
"""

response = client.converse(
    modelId=MODEL_ID,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "text": prompt
                },
                {
                    "image": {
                        "format": "png",
                        "source": {
                            "bytes": image_bytes
                        }
                    }
                }
            ]
        }
    ],
    inferenceConfig={
        "maxTokens": 800,
        "temperature": 0.2
    }
)

print("\n===== CIRCUIT DOCTOR =====\n")

print(
    response["output"]["message"]["content"][0]["text"]
)

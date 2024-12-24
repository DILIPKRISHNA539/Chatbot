from flask import Flask, request, render_template
from gradio_client import Client

# Initialize Flask app
app = Flask(__name__)

# Gradio Client configuration
client = Client("tencent/Hunyuan-Large")  # Replace with desired model

def query_gradio(message):
    """Send a request to the Gradio API."""
    try:
        result = client.predict(
            message=message,
            api_name="/chat"
        )
        return result
    except Exception as e:
        return {"error": str(e)}

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    user_message = ""
    bot_reply = ""
    
    if request.method == 'POST':
        # Get the user's message from the form
        user_message = request.form.get("message", "")
        
        if user_message:
            # Send the message to the Gradio model API
            bot_reply = query_gradio(user_message)

            # If the response is an error
            if "error" in bot_reply:
                bot_reply = "Sorry, there was an error processing your request."
            else:
                bot_reply = bot_reply.strip()

    return render_template('index.html', user_message=user_message, bot_reply=bot_reply)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)

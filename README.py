import telebot  
import requests  
import time  

# Tumhara BotFather token  
BOT_TOKEN = "7568199727:AAFNC22rwUnDV7DBDpXx-ibKoJUgrcedGfM"  
# Tumhari Replicate API key  
REPLICATE_API_KEY = "r8_1fcrCidDqrI18HVYnXqQYXMLVpHV35r4co3x8"  

bot = telebot.TeleBot(BOT_TOKEN)

# Ghibli-style image generation function
def generate_ghibli_image(prompt):
    # Replicate API endpoint  
    MODEL_URL = "https://api.replicate.com/v1/predictions"
    
    headers = {
        "Authorization": f"Token {REPLICATE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "version": "f178c7088d15...",  # SDXL ya Anything V5 ka model version ID  
        "input": {
            "prompt": f"Ghibli-style: {prompt}",
            "width": 1024,
            "height": 1024,
            "num_outputs": 1
        }
    }

    response = requests.post(MODEL_URL, headers=headers, json=data)

    if response.status_code == 201:
        prediction_id = response.json()["id"]

        # Wait for the prediction to complete
        while True:
            prediction_url = f"{MODEL_URL}/{prediction_id}"
            prediction_response = requests.get(prediction_url, headers=headers)
            status = prediction_response.json()["status"]

            if status == "succeeded":
                image_url = prediction_response.json()["output"][0]
                return image_url
            elif status == "failed":
                return "Error: Image generation failed."
            
            time.sleep(5)  # Wait before checking again
    else:
        return "Error: Couldn't connect to Replicate."

# Start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Hello! Mujhe koi bhi Ghibli scene ya idea bhejo aur main uska image banaunga!")

# Message handler
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    prompt = message.text
    bot.send_message(message.chat.id, "⏳ Image generate ho rahi hai...")

    image_url = generate_ghibli_image(prompt)

    if "Error" in image_url:
        bot.send_message(message.chat.id, "⚠️ Image banane mein problem aayi.")
    else:
        bot.send_photo(message.chat.id, image_url)

# Start the bot  
bot.polling()

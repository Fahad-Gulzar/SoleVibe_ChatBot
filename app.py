
from flask import Flask, render_template, request
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

PRODUCTS = {
    "Running Shoes": {
        "brand": "AeroRun",
        "sizes": ["7", "8", "9", "10"],
        "material": "Mesh + Rubber Sole",
        "colors": ["Red", "Black", "Blue"],
        "price": "$89.99"
    },
    "Casual Sneakers": {
        "brand": "UrbanStep",
        "sizes": ["6", "7", "8", "9"],
        "material": "Canvas + Rubber Sole",
        "colors": ["White", "Grey", "Navy"],
        "price": "$74.50"
    },
    "Formal Leather Shoes": {
        "brand": "EliteWear",
        "sizes": ["7", "8", "9"],
        "material": "Genuine Leather",
        "colors": ["Black", "Brown"],
        "price": "$129.00"
    },
    "Kids Shoes": {
        "brand": "LittleSteps",
        "sizes": ["1", "2", "3"],
        "material": "Synthetic",
        "colors": ["Pink", "Yellow", "Blue"],
        "price": "$49.99"
    }
}
faq_section = """
SoleVibe FAQ:

Q: What is your return policy?
A: We accept returns within 30 days for unworn shoes with original packaging.

Q: Do you offer free shipping?
A: Yes, free shipping is offered for all orders above $50.

Q: How long does delivery take?
A: Orders are usually delivered within 3–5 business days.

Q: Can I exchange sizes?
A: Yes, we offer one free size exchange per order.

"""

@app.route("/")
def home():
    return render_template("products.html")

@app.route("/products")
def products():
    return render_template("products.html", products=PRODUCTS)

@app.route("/customer-service")
def customer_service():
    return render_template("chat.html")

@app.route("/get", methods=["POST"])
def get_response():
    user_msg = request.form["msg"]

    # Build context string with all product details
    context = "SoleVibe Product Catalog:\n"
    for product, details in PRODUCTS.items():
        context += f"- {product}\n"
        context += f"  Brand: {details['brand']}\n"
        context += f"  Sizes: {', '.join(details['sizes'])}\n"
        context += f"  Material: {details['material']}\n"
        context += f"  Colors: {', '.join(details['colors'])}\n"
        context += f"  Price: {details['price']}\n\n"

    prompt = f"""You are a helpful customer service chatbot for SoleVibe.
Use the product catalog and FAQ section below to answer questions.

{context}
{faq_section}
Customer: {user_msg}
"""

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)


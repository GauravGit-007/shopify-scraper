Shopify Product Scraper is a Flask-based web application that allows users to extract publicly available product information from any Shopify store using its open JSON endpoints. With just the store URL, the tool fetches all accessible product details and presents them in a clean and organized format. It's designed to be simple, fast, and reliable for users who need to analyze or monitor Shopify store products.

🔍 Key Features:
Easy to Use Interface: Users simply paste the Shopify store URL into the form and submit. No technical knowledge is required.

POST & GET Support: The application supports both manual browsing and programmatic access via an API route (/api/scrape), making it suitable for developers and non-developers alike.

Clean Data Output: The scraper collects essential product information such as:

Title

Price

Images

Product Handle

Product Type

Inventory and more (based on what's publicly available)

Built on Flask: Lightweight and extendable, with routes managed in routes.py.

Error Handling: If the URL is invalid, unreachable, or not a Shopify store, proper error messages are shown on the frontend and via JSON on the API.

🛠️ Technologies Used:
Python 3

Flask (for backend server and routing)

Jinja2 (for templating)

HTML/CSS (for frontend form)

requests library (for handling HTTP requests)

📦 Use Cases:
Competitor research for Shopify stores

Academic projects or demos in web scraping

Product data analysis for marketing or inventory tools

The project is modular and easy to customize. Developers can enhance it by adding database support, authentication, pagination, or integrating with data visualization tools.

Note: This tool only scrapes data that Shopify stores publicly expose via their .json endpoints. It does not violate any security protocols or scrape protected/private data.

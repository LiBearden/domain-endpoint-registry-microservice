# Import the Flask framework
from flask import Flask, jsonify
from pymongo import MongoClient
import os
import markdown

# Create an instance of Flask
app = Flask(__name__)
cluster = MongoClient("mongodb+srv://dbAdmin:<password>@endpoint-generator-db.uyveq.gcp.mongodb.net/domain-data?retryWrites=true&w=majority")
db = cluster["domain-data"]
collection = db["domains"]


@app.route('/', methods=['GET'])
def index():
    """Present the documentation from the README.md file."""
    # Open the documentation README file
    with open(os.path.dirname(app.root_path) + "/README.md", "r") as markdown_file:
        # Read the content of the file
        content = markdown_file.read()
        # Convert the file content to HTML
        return markdown.markdown(content)


@app.route('/domains', methods=['GET'])
def get_all_domains():
    domains = collection.find()
    results = []
    for domain in domains:
        results.append({"name": domain["name"], "added-date": domain["added-date"], "events": domain["events"]})
    return jsonify({"items": results})



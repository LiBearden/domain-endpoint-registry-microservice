# Import necessary packages
from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime
import os
import markdown

# Create an instance of Flask and prevent it from sorting JSON attributes
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Initialize MongoDB Atlas for database operations
cluster = MongoClient("mongodb+srv://MONGO_SRV_URI")
db = cluster["domain-data"]
collection = db["domains"]


# Initialize the root route and expose endpoint to GET for documentation reference
@app.route('/', methods=['GET'])
def index():
    """Present the documentation from the README.md file."""
    # Open the documentation README file
    with open(os.path.dirname(app.root_path) + "/README.md", "r") as markdown_file:
        # Read the content of the file
        content = markdown_file.read()
        # Convert the file content to HTML
        return markdown.markdown(content)


# Initialize "/domains" endpoint, allow GET method to retrieve a list of all domains
@app.route('/domains', methods=['GET'])
def get_all_domains():
    domains = collection.find()
    results = []
    for domain in domains:
        results.append({"name": domain["name"], "added-date": datetime.fromisoformat(str(domain["added-date"])), "events": domain["events"]})
    return jsonify({"items": results})


# Initialize "/domains" endpoint, allow POST method to add new domains

@app.route('/domains', methods=['POST'])
def add_domain():
    domains = collection
    name = request.json["name"]
    events = request.json["events"]
    post = {"name": name, "events": events, "added-date": str(datetime.utcnow())}
    domain_id = domains.insert_one(post).inserted_id
    new_domain = domains.find_one({"_id": domain_id})
    results = {
        "name": new_domain["name"],
        "added-date": new_domain["added-date"],
        "events": new_domain["events"]
    }
    return {"items": results}


# Initialize custom domain name endpoint with the GET method to retrieve a single domain
@app.route('/domains/<name>', methods=['GET'])
def get_one_domain(name):
    domains = collection
    domain = domains.find_one({"name": name})
    result = {"items": {"name": domain["name"], "added-date": domain["added-date"], "events": domain["events"]}}
    return jsonify(result)


# Initialize custom domain name endpoint with the DELETE method to delete a single domain
@app.route('/domains/<name>', methods=['DELETE'])
def delete_domain(name):
    domains = collection
    domain = domains.find_one({"name": name})
    deleted_domain = domains.delete_one(domain)
    results = {
                "name": domain["name"],
                }
    return {"deleted_items": results, "message": "Domain deleted successfully."}






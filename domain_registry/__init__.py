# Import the Flask framework
from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime
import os
import markdown

# Create an instance of Flask
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
cluster = MongoClient("mongodb+srv://domainRegistry:LBLrWRelu8AKelBw@endpoint-generator-db.vmequ.gcp.mongodb.net/domain-data?retryWrites=true&w=majority")
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
        results.append({"name": domain["name"], "added-date": datetime.fromisoformat(str(domain["added-date"])), "events": domain["events"]})
    return jsonify({"items": results})


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


@app.route('/domains/<name>', methods=['GET'])
def get_one_domain(name):
    domains = collection
    domain = domains.find_one({"name": name})
    result = {"items": {"name": domain["name"], "added-date": domain["added-date"], "events": domain["events"]}}
    return jsonify(result)


@app.route('/domains/<name>', methods=['DELETE'])
def delete_domain(name):
    domains = collection
    domain = domains.find_one({"name": name})
    deleted_domain = domains.delete_one(domain)
    results = {
                "name": domain["name"],
                }
    return {"deleted_items": results, "message": "Domain deleted successfully."}






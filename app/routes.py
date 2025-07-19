from flask import Blueprint, request, jsonify, render_template, Response
from app.scraper import scrape_shopify_store
import requests
import csv
import io

bp = Blueprint('routes', __name__)

@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("website_url")
        if not url:
            return render_template("form.html", error="Please provide a URL")

        try:
            r = requests.get(url, timeout=5)
            if r.status_code != 200:
                return render_template("form.html", error="Website not reachable")

            data = scrape_shopify_store(url)
            return render_template("form.html", data=data, url=url)

        except Exception as e:
            return render_template("form.html", error=f"Error: {str(e)}")

    return render_template("form.html")


@bp.route("/api/scrape", methods=["POST"])
def api_scrape():
    json_data = request.get_json()
    if not json_data or "website_url" not in json_data:
        return jsonify({"error": "Missing 'website_url' in JSON body"}), 400

    url = json_data["website_url"]

    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return jsonify({"error": "Website not reachable"}), 401

        data = scrape_shopify_store(url)
        return jsonify({
            "success": True,
            "scraped_data": data,
            "source_url": url
        })

    except Exception as e:
        return jsonify({"error": f"Internal error: {str(e)}"}), 500


@bp.route("/download-csv", methods=["POST"])
def download_csv():
    website_url = request.form.get("website_url")
    if not website_url:
        return "Missing website_url", 400

    try:
        r = requests.get(website_url, timeout=5)
        if r.status_code != 200:
            return "Website not reachable", 400

        data = scrape_shopify_store(website_url)
        if not data:
            return "No data to download", 400

        # Create CSV in-memory
        si = io.StringIO()
        writer = csv.DictWriter(si, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        output = si.getvalue()
        si.close()

        return Response(
            output,
            mimetype="text/csv",
            headers={"Content-Disposition": f"attachment; filename=scraped_data.csv"}
        )

    except Exception as e:
        return f"Error generating CSV: {str(e)}", 500

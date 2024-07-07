from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

ORGANIZATION_API_URL = "https://www.eventbriteapi.com/v3/users/me/organizations/"
EVENT_API_URL = "https://www.eventbriteapi.com/v3/organizations/{}/events/"
EVENT_API_KEY = "NQFYW5CJPK4N7SXTNBA7"

@app.route("/organizations", method=["GET"])
def search_organizations():
  response = requests.get(
    ORGANIZATION_API_URL,
    headers={"Authorization": f"Bearer {EVENT_API_KEY}"},
  )
  # {
  #   organizations: (_type, name, vertical, parent_id, locale, created, image_id, id)[],
  #   pagination: (object_coun, continuation, page_count, page_size, has_more_items, page_number)
  # }
  return response

@app.route("/search_by_organization", methods=["GET"])
def search_events_by_organization():
  organization_id = request.args.get("organization_id", "")
  search_criteria = {
    "status": request.args.get("status", ""),
    "time_filter": request.args.get("time_filter", ""),
    "currency_filter": request.args.get("currency_filter", ""),
    "order_by": request.args.get("order_by", ""),
  }

  response = requests.get(
    EVENT_API_URL.format(organization_id),
    headers={"Authorization": f"Bearer {EVENT_API_KEY}"},
    params=search_criteria,
  )

  events = response.json().get("events", [])
  return jsonify(events)


if __name__ == "__main__":
  app.run(debug=True)

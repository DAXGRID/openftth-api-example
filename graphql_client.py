#!/usr/bin/env python3
"""
Minimal GraphQL client.
1. Fetch an OAuth2 token using client credentials.
2. POST the GraphQL request with the token as a Bearer header.
"""

import json
import urllib.parse
import urllib.request


def get_token(token_endpoint, client_id, client_secret):
    body = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }).encode()

    request = urllib.request.Request(token_endpoint, data=body, method="POST")
    request.add_header("Content-Type", "application/x-www-form-urlencoded")

    with urllib.request.urlopen(request) as response:
        return json.load(response)["access_token"]


def send_graphql(graphql_address, token, query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()

    request = urllib.request.Request(graphql_address, data=body, method="POST")
    request.add_header("Content-Type", "application/json")
    request.add_header("Authorization", f"Bearer {token}")

    with urllib.request.urlopen(request) as response:
        return json.load(response)

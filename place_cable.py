#!/usr/bin/env python3
"""
Example of placing a cable (span equipment) in the route network via the
OpenFTTH API gateway.

Usage:
    python3 place_cable.py \
        --client-id ... --client-secret ... \
        --token-endpoint ... --graphql-address ... \
        --span-equipment-specification-id <spec-guid> \
        --route-segment-ids <segment-guid> <segment-guid> ... \
        [--name K12345]
"""

import argparse
import json
import sys
import uuid

from graphql_client import get_token, send_graphql


PLACE_SPAN_EQUIPMENT_MUTATION = """
mutation (
  $spanEquipmentId: ID!,
  $spanEquipmentSpecificationId: ID!,
  $routeSegmentIds: [ID]!,
  $manufacturerId: ID,
  $namingInfo: NamingInfoInput,
  $markingInfo: MarkingInfoInput
) {
  spanEquipment {
    placeSpanEquipmentInRouteNetwork(
      spanEquipmentId: $spanEquipmentId,
      spanEquipmentSpecificationId: $spanEquipmentSpecificationId,
      routeSegmentIds: $routeSegmentIds,
      manufacturerId: $manufacturerId,
      namingInfo: $namingInfo,
      markingInfo: $markingInfo
    ) {
      isSuccess
      errorCode
      errorMessage
    }
  }
}
"""


def check_errors(response):
    if response.get("errors"):
        for error in response["errors"]:
            print(error.get("message"), file=sys.stderr)
        sys.exit("Received error response back from GraphQL.")


def main():
    parser = argparse.ArgumentParser(description="Place a cable in the route network via GraphQL.")
    parser.add_argument("--client-id", required=True)
    parser.add_argument("--client-secret", required=True)
    parser.add_argument("--token-endpoint", required=True)
    parser.add_argument("--graphql-address", required=True)
    parser.add_argument("--span-equipment-specification-id", required=True)
    parser.add_argument("--route-segment-ids", required=True, nargs="+")
    parser.add_argument("--span-equipment-id", default=str(uuid.uuid4()))
    parser.add_argument("--manufacturer-id")
    parser.add_argument("--name")
    parser.add_argument("--description")
    parser.add_argument("--marking-color")
    parser.add_argument("--marking-text")
    args = parser.parse_args()

    token = get_token(args.token_endpoint, args.client_id, args.client_secret)

    variables = {
        "spanEquipmentId": args.span_equipment_id,
        "spanEquipmentSpecificationId": args.span_equipment_specification_id,
        "routeSegmentIds": args.route_segment_ids,
        "manufacturerId": args.manufacturer_id,
        "namingInfo": {"name": args.name, "description": args.description},
        "markingInfo": {"markingColor": args.marking_color, "markingText": args.marking_text},
    }

    response = send_graphql(args.graphql_address, token, PLACE_SPAN_EQUIPMENT_MUTATION, variables)
    check_errors(response)

    result = response["data"]["spanEquipment"]["placeSpanEquipmentInRouteNetwork"]
    if not result["isSuccess"]:
        sys.exit(f"Failed with errorcode: '{result['errorCode']}' and error message: '{result['errorMessage']}'.")

    print(json.dumps({"spanEquipmentId": args.span_equipment_id, **result}))


if __name__ == "__main__":
    main()

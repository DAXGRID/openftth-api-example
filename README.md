# OpenFTTH Api Example

Example Python script for calling the OpenFTTH GraphQL API. It authenticates with OAuth2 client credentials and only uses the Python standard library.

## Place a cable

`place_cable.py` places a cable (span equipment) in the route network along the given route segments.

```sh
python3 place_cable.py \
    --client-id example-client \
    --client-secret my-super-duper-secret \
    --token-endpoint https://auth.example.com/realms/openftth/protocol/openid-connect/token \
    --graphql-address https://api.example.com/graphql \
    --span-equipment-id ce93f216-f7ab-446a-b67d-227b8cd2a626 \
    --span-equipment-specification-id 64023c04-c866-4e6f-9978-770bbb69488d \
    --route-segment-ids 14d7b0d2-e7e8-43c8-9b14-c3f359bf7df6 2660c452-5b6e-4a5d-a5cd-6306d702734f \
    --marking-color "ORANGE MED RØD STRIBE" \
    --marking-text 1234
```

Optional arguments: `--span-equipment-id` (a random ID is used if you leave it out), `--manufacturer-id`, `--description`, `--marking-color`, `--marking-text`.

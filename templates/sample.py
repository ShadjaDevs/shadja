import jinja2

sample = {
  "560090": [
    {
      "center_id": 418395,
      "name": "Murphy Town UPHC",
      "address": "Nala Road Murphy Town",
      "state_name": "Karnataka",
      "district_name": "BBMP",
      "block_name": "East",
      "pincode": 560008,
      "lat": 12,
      "long": 77,
      "from": "09:00:00",
      "to": "18:00:00",
      "fee_type": "Free",
      "sessions": [
        {
          "session_id": "8886e694-7735-460b-83f1-4d6fe36d8605",
          "date": "05-05-2021",
          "available_capacity": 39,
          "min_age_limit": 45,
          "vaccine": "COVISHIELD",
          "slots": [
            "09:00AM-11:00AM",
            "11:00AM-01:00PM",
            "01:00PM-03:00PM",
            "03:00PM-06:00PM"
          ]
        },
        {
          "session_id": "9a378a76-8879-450f-81b2-fd36ad29b996",
          "date": "06-05-2021",
          "available_capacity": 13,
          "min_age_limit": 45,
          "vaccine": "COVISHIELD",
          "slots": [
            "09:00AM-11:00AM",
            "11:00AM-01:00PM",
            "01:00PM-03:00PM",
            "03:00PM-06:00PM"
          ]
        }
      ]
    },
    {
      "center_id": 418365,
      "name": "Kodihalli UPHC Covi-S",
      "address": "Old Airport Road Next To Manipal Hospital",
      "state_name": "Karnataka",
      "district_name": "BBMP",
      "block_name": "East",
      "pincode": 560008,
      "lat": 12,
      "long": 77,
      "from": "09:00:00",
      "to": "18:00:00",
      "fee_type": "Free",
      "sessions": [
        {
          "session_id": "3c8cb9d6-45f7-425e-9425-3e5ab47a522c",
          "date": "06-05-2021",
          "available_capacity": 0,
          "min_age_limit": 45,
          "vaccine": "COVISHIELD",
          "slots": [
            "09:00AM-11:00AM",
            "11:00AM-01:00PM",
            "01:00PM-03:00PM",
            "03:00PM-06:00PM"
          ]
        }
      ]
    },
    {
      "center_id": 572901,
      "name": "KODIHALLI UPHC COVAXIN",
      "address": "Old Airport Road Indiranagar",
      "state_name": "Karnataka",
      "district_name": "BBMP",
      "block_name": "East",
      "pincode": 560008,
      "lat": 12,
      "long": 77,
      "from": "09:00:00",
      "to": "18:00:00",
      "fee_type": "Free",
      "sessions": [
        {
          "session_id": "9666077b-6850-4ab7-8bdd-9990f6eac712",
          "date": "06-05-2021",
          "available_capacity": 0,
          "min_age_limit": 45,
          "vaccine": "COVAXIN",
          "slots": [
            "09:00AM-11:00AM",
            "11:00AM-01:00PM",
            "01:00PM-03:00PM",
            "03:00PM-06:00PM"
          ]
        }
      ]
    },
    {
      "center_id": 559097,
      "name": "C V Raman Hospital Block 2",
      "address": "4th B Cross Rd Kalyan Nagar",
      "state_name": "Karnataka",
      "district_name": "BBMP",
      "block_name": "East",
      "pincode": 560008,
      "lat": 12,
      "long": 77,
      "from": "09:00:00",
      "to": "18:00:00",
      "fee_type": "Free",
      "sessions": [
        {
          "session_id": "9f3d23a9-40b2-4880-aaef-9e22056f958b",
          "date": "07-05-2021",
          "available_capacity": 0,
          "min_age_limit": 45,
          "vaccine": "COVISHIELD",
          "slots": [
            "09:00AM-11:00AM",
            "11:00AM-01:00PM",
            "01:00PM-03:00PM",
            "03:00PM-06:00PM"
          ]
        }
      ]
    }
  ]
}

rendered = jinja2.Template(open('email_slot_template.html').read()).render(available_centers=sample)

print(rendered)
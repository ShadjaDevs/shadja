
# Input format
For APIs which require input data, format is always JSON

# Output format
JSON output: a hash with the following keys:

1. 'success' key: A boolean, always present. Indicates success/failure of the API call. Also coupled with the suitable response code (200/400)

2. 'error' key: A string, present when API sets 'success' to false. Also coupled with the suitable response code (400). Contains the error message describing the cause of failure.

3. other keys: 'uuid', 'subscription' etc. based on the endpoint

# /add_subscription

Method: POST
JSON input

## required
  - old: bool
  - pincodes: list of integers

## optional
  - want_free: bool,
  - flavor: str,
  - start_date: str,
  - end_date: str,
  - email: str,
  - mobile: int,
  - telegram_id: str
Response (on success): uuid in JSON format

# /update_subscription/<uuid>

Method: POST
JSON input: hash with keys to be updated for the given subscription.
Valid keys: all keys present in the 200 response for `/get_subscription` endpoint.
Response (on success): uuid in JSON format

Note:
  - Verified email/mobile/telegram ID cannot be edited
  - New email/mobile/telegram ID can be added if not present already

# /get_subscription/<uuid>

Method: GET
JSON input: None

Response (on success): 'subscription' key in the hash containing all attributes corresponding to the uuid.

# /remove_subscription/<uuid>

Method: GET
JSON input: None

Response (on success): 'success' key set to true

Note: this method is implemented as 'GET' instead of 'DELETE' so that the link can be embedded in notification emails/SMS and users have a one click unsubscribe experience.

# /input_otp/<uuid>

Method: POST
JSON input: hash with following keys:
  - 'otp_email' containing 4 digit email OTP
  - 'otp_mobile' containing 4 digit mobile OTP^

Note:
  - Mobile OTP not implemented yet
  - Hash may only contain one or more of the keys based on what notification channels are selected.

Response
  - on success: 'success' key set to true
  - on failure: 'success' key set to false

# /nearby_pincodes/<pincode>/<radius>

Method: GET
JSON input: None

Response (on success):
A hash with 'pincodes' key containing a list of pincodes which are within a circle of `radius` km from `pincode`.

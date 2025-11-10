# AI Fashion Stylist API - Testing Guide (V1)

This document provides a complete set of cURL commands to test every endpoint of the V1 API.

**Base URL:** `http://127.0.0.1:8000`

---

## Step 1: Setup and Authentication

Before testing, run these commands in your terminal. They will register a test user, log in, and save the authentication token to a shell variable (`$TOKEN`) for easy reuse.

**Note:** You only need to run the `curl` command for registration once.

```bash
# --- 1. Set your desired username and password ---
export USERNAME="testuser"
export PASSWORD="password123"

# --- 2. Register the user (only need to run this once per user) ---
echo "Registering user '$USERNAME'..."
curl -X 'POST' \
  'http://127.0.0.1:8000/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "'"$USERNAME"'",
    "password": "'"$PASSWORD"'"
  }'
echo "\n"

# --- 3. Login and capture the access token ---
echo "Logging in and capturing token..."
export TOKEN=$(curl -X 'POST' \
  'http://127.0.0.1:8000/token' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username='"$USERNAME"'&password='"$PASSWORD"'' \
  | sed -E 's/.*"access_token":"([^"]+)".*/\1/')

# --- 4. Verify that the TOKEN variable is set ---
echo "---"
echo "Setup complete. Your token is:"
echo "$TOKEN"
echo "---"
```

---

## Step 2: Test the API Endpoints

### User Endpoints

#### Get Current User Details
*   **Description:** Retrieves the details of the currently authenticated user.
*   **Endpoint:** `GET /users/me`
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/users/me' \
  -H 'accept: application/json' \
  -H "Authorization: Bearer $TOKEN"
```

---

### Wardrobe Endpoints

#### Create a New Wardrobe Item
*   **Description:** Adds a new clothing item to the user's wardrobe.
*   **Endpoint:** `POST /wardrobe/`
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/wardrobe/' \
  -H 'accept: application/json' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Vintage Leather Jacket",
    "item_metadata": {
      "category": "outerwear",
      "style": "edgy",
      "color": "brown",
      "material": "leather",
      "formality": 5,
      "properties": ["durable", "wind-resistant"]
    }
  }'
```

#### Get All Wardrobe Items
*   **Description:** Retrieves a list of all items in the user's wardrobe.
*   **Endpoint:** `GET /wardrobe/`
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/wardrobe/' \
  -H 'accept: application/json' \
  -H "Authorization: Bearer $TOKEN"
```

#### Update a Wardrobe Item
*   **Description:** Updates the details of a specific clothing item.
*   **Note:** Replace `{ITEM_ID}` with an actual ID from the "Get All" response above.
*   **Endpoint:** `PUT /wardrobe/{item_id}`
```bash
# Example for item_id = 1
curl -X 'PUT' \
  'http://127.0.0.1:8000/wardrobe/1' \
  -H 'accept: application/json' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Vintage Brown Leather Jacket",
    "item_metadata": {
      "category": "outerwear",
      "style": "vintage-edgy",
      "color": "dark-brown",
      "material": "leather",
      "formality": 6,
      "properties": ["durable", "wind-resistant"]
    }
  }'
```

#### Delete a Wardrobe Item
*   **Description:** Removes a specific clothing item from the wardrobe.
*   **Note:** Replace `{ITEM_ID}` with an actual ID. A successful delete returns a `204 No Content` status.
*   **Endpoint:** `DELETE /wardrobe/{item_id}`
```bash
# Example for item_id = 1
curl -X 'DELETE' \
  -v \
  'http://127.0.0.1:8000/wardrobe/1' \
  -H 'accept: application/json' \
  -H "Authorization: Bearer $TOKEN"
```

---

### AI Stylist Endpoint

#### Get an AI Style Suggestion
*   **Description:** Generates an AI outfit suggestion based on the user's current wardrobe.
*   **Endpoint:** `POST /style-me/`
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/style-me/' \
  -H 'accept: application/json' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "occasion": "A casual friday at the office",
    "weather_context": "Cool and rainy, around 55°F"
  }'
```
from fastapi import APIRouter, HTTPException
import httpx
from keys import GOOGLE_MAPS_API_KEY

router = APIRouter()

@router.get("/get-location")

async def get_location():
    # Get the geolocation (latitude and longitude)
    get_location_url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={GOOGLE_MAPS_API_KEY}"
    
    payload = {
        "considerIp": "true"  # Use IP-based geolocation
    }

    try:
        async with httpx.AsyncClient() as client:
            # Send a request to get the geolocation (lat, lng)
            location_response = await client.post(get_location_url, json=payload)
            location_response.raise_for_status()

            # Parse the location data
            location_data = location_response.json()

            # Extract latitude and longitude
            lat = location_data['location']['lat']
            lng = location_data['location']['lng']

            #reverse geocoding that shit
            get_address_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={GOOGLE_MAPS_API_KEY}"

            #send a request to get the address
            address_response = await client.get(get_address_url)
            address_response.raise_for_status()

            address_data = address_response.json()

            # chk if there are any results and return the first formatted address
            if "results" in address_data and len(address_data["results"]) > 0:
                address = address_data["results"][0]["formatted_address"]
                return address  # Return the address as a string
            else:
                raise HTTPException(status_code=404, detail="Address not found")

    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail="Error fetching location or address")




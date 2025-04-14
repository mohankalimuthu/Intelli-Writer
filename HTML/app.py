import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

# Load Gemini API key
genai.configure(api_key="AIzaSyA-bvO22mIvxWGKrM_ZTHHCnN52htvsWF0")

model = genai.GenerativeModel("gemini-1.5-pro")

app = Flask(__name__)
CORS(app)  # Enables cross-origin requests

@app.route('/generate_fir', methods=['POST'])
def generate_fir():
    try:
        data = request.json  # Get FIR input details

      
        prompt = f"""
        You are an expert legal assistant. Based on the details provided, generate a formal First Information Report (FIR):

        Complainant Details:
        - Name: {data.get('complainant_name', 'Unknown')}
        - Mobile: {data.get('complainant_mobile', 'Unknown')}
        - Address: {data.get('complainant_address', 'Unknown')}

        Accused Details:
        - Name: {data.get('accused_name', 'Unknown')}
        - Mobile: {data.get('accused_mobile', 'Unknown')}
        - Address: {data.get('accused_address', 'Unknown')}

        Officer Details:
        - Name: {data.get('officer_name', 'Unknown')}
        - Rank: {data.get('officer_rank', 'Unknown')}
        - District: {data.get('district', 'Unknown')}
        - Police Station: {data.get('police_station', 'Unknown')}

        Incident Details:
        - Date: {data.get('incident_date', 'Unknown')}
        - Time: {data.get('incident_time', 'Unknown')}
        - Location: {data.get('incident_location', 'Unknown')}
        - Description: {data.get('incident_details', 'No details provided')}

        Write a structured and professional FIR report based on these details.
        """

        
        response = model.generate_content(prompt)
        print(response)

        
        
        # Ensure correct extraction of text
        if hasattr(response, "parts") and response.parts:
            fir_description = response.parts[0].text
        else:
            fir_description = "Error: No response from Gemini API."

        print("Final Generated Description:", fir_description)  # Debugging
        return jsonify({"description": fir_description})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

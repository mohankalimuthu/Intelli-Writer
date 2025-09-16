import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime





genai.configure(api_key="##########")

model = genai.GenerativeModel("gemini-1.5-pro")

app = Flask(__name__)
CORS(app)  

@app.route('/generate_fir', methods=['POST'])
def generate_fir():
    try:
        data = request.json  
        now = datetime.now()
        fir_number = f"FIR-{now.strftime('%d%m%Y-%H%M')}"  # FIR-DDMMYYYY-HHMM
        fir_date = now.strftime("%Y-%m-%d")  # YYYY-MM-DD
        fir_time = now.strftime("%H:%M:%S")  # HH:MM:SS
        
        
        prompt = f"""
You are an expert legal assistant. Based on the details provided, generate a formal First Information Report (FIR): Generate a structured First Information Report (FIR) based on the provided details. Do not use any bold formatting for any headings. The FIR should be structured as follows:

FIRST INFORMATION REPORT (FIR)

Police Station: {data.get('police_station', 'Unknown')}
District: {data.get('district', 'Unknown')}
FIR No.: {fir_number}
Date: {fir_date}
Time: {fir_time}

Complainant Information:
 Name: {data.get('complainant_name', 'Unknown')}
 Mobile No.: {data.get('complainant_mobile', 'Unknown')}
 Address: {data.get('complainant_address', 'Unknown')}

Accused Information:
 Name: {data.get('accused_name', 'Unknown')}
 Mobile No.: {data.get('accused_mobile', 'Unknown')}
 Address: {data.get('accused_address', 'Unknown')}

Officer In-Charge:
 Name: {data.get('officer_name', 'Unknown')}
 Rank: {data.get('officer_rank', 'Unknown')}

Information Received From: {data.get('complainant_name', 'Unknown')}

Date of Offence: {data.get('incident_date', 'Unknown')}
Time of Offence: {data.get('incident_time', 'Unknown')}
Place of Offence: {data.get('incident_location', 'Unknown')}

Incident Description:
{data.get('incident_details', 'No details provided')}

Ensure that the FIR is formatted **without any bold formatting at all** for any section headings. Everything should be written in a normal readable format.  Write a structured and professional FIR report based on these details.
"""


        
        response = model.generate_content(prompt)

        
        
        
        if hasattr(response, "parts") and response.parts:
            fir_description = response.parts[0].text
        else:
            fir_description = "Error: No response from Gemini API."

        #print("Final Generated Description:", fir_description)  # Debugging
        return jsonify({"description": fir_description})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

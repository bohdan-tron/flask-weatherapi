from flask import Flask, render_template
import requests
import pandas as pd


app = Flask(__name__)

stations = pd.read_csv("weather-data-small/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 "]]

@app.route('/')
def home():
  return render_template('home.html', data=stations.to_html())

  
@app.route('/api/v1/<station>/<date>')
def api(station, date):
  filename = f"weather-data-small/TG_STAID{station:>06}.txt"
  df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
  temperature = df.loc[df["    DATE"] == date]['   TG'].squeeze() / 10
  return {
    "station": station,
    "date": date,
    "temperature": temperature,
  }

    
@app.route('/api/v0/<word>')
def word(word):
  """
    Extract word definition from https://api.dictionaryapi.dev
  """
  try:
    r = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    if r.status_code == 200:
      data = r.json()
      
      # Extract definition
      definition = []
      if data and len(data) > 0:
        
        for meaning in data[0].get("meanings", []):
          
          for index, definition_item in enumerate(meaning.get("definitions", [])):
            
            definition_text = definition_item.get("definition", "")
            definition_text = f"{index + 1}. {definition_text};"
            definition.append( definition_text + '\n')
            
      definition = " ".join(definition)
      
  except Exception as e:
    return {
      "word": word,
      "error": f"An error occurred: {str(e)}"
    }
            
  return {
    "definition": definition,
    "word": word,
  }

if __name__ == '__main__':
  app.run(debug=True, port=5001)
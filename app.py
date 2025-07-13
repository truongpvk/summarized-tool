from flask import Flask, render_template, request, jsonify
import os
from summarizer.extractive.model import extract_top_n_sentences
from summarizer.abstractive.model import create_prompt, get_response

template_folder = os.path.join("templates")

app = Flask(__name__, template_folder=template_folder)

@app.route('/')
def index():
  return render_template("index.html")


# Read input and summarize text
@app.route('/summarize', methods=["POST", "GET"])
def summarize():
  text = request.args.get('text', '')
  mode = request.args.get('mode', '0')
  
  if not text.strip():
    return jsonify({"error": "No text provided"}), 400

  if mode == '0':
    summary = extract_top_n_sentences(text, n=3)
  else:
    summary = get_response(create_prompt(text))
  
  return jsonify({
    "summary": summary,
    "mode": int(mode),
    "original_length": len(text),
    "summary_length": len(summary)
  })


# Save result and time to response each case
@app.route('/save_response', methods=['POST'])
def save():
  import json
  
  path = os.path.join("summarizer", "log_data", "response.json")
  try:
    with open(path, 'r', encoding='utf-8') as f:
      log = json.load(f)
    
    if not log:
      log = []
  except:
    log = []
  
  
  try:
    data = request.get_json()

    input_text = data.get('input')
    response_text = data.get('response')
    mode = data.get('mode')
    time = data.get('time')

    from datetime import datetime
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    entry = {
      "timestamp": timestamp,
      "input": input_text,
      "response": response_text,
      "mode": mode,
      "time": time
    }
    
    log.append(entry)
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(log, f, indent=4, ensure_ascii=False)
    
    
    return jsonify({'success': True})
    
  except Exception as e:
    return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
  app.run(debug=True)



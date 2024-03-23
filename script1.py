import google.generativeai as genai
import csv

genai.configure(api_key="AIzaSyDFm0HcBBVc-k3P_UxudP_3iXEOaIItcKM")

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 5048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Open the CSV file and iterate through each row
with open('songs.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        album = row['Album']
        year = row['Year']
        track_number = row['Track Number']
        song_title = row['Song Title']
        lyrics = row['Lyrics']

        prompt_parts = [
            # Your prompt, using the values from the current row
            f"\"\"\"using the following lyrics as reference please compile 10 keywords or \"tags\" capturing the subects and themes of the the piece. Then compile a brief introductory summary of the piece placing in the the contect of the album and track number. Then iterate and factore in varying perspectives and compile an essay for a weekly feature blog post celebrating the lyrics of gorr dowie. Output all as follow\n\n---\nTitle: {song_title}\nImage: \"{song_title.replace(' ', '').lower()}plus.jpg\"\ndate: TBD\nTags: \"Add your to keywords\"\n---\n\n{{< tabs >}}\n\n## Lyrics\n\n{lyrics}\n\n## References\n\nADD your keyword reference\n\n## Essay\n\nAdd your feature blog entry a tribute and celebration of Gord Downies lyrics\n\n\"\"\""
        ]

        response = model.generate_content(prompt_parts)

        # Save the output to a text file
        with open(f"{song_title.replace(' ', '_')}.txt", 'w', encoding='utf-8') as file:
            file.write(response.text)
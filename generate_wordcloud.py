import argparse
import csv
import string
import os
from collections import Counter
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

def read_text_file(filepath):
    """Reads text content from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        raise RuntimeError(f"Error reading file {filepath}: {e}")

def process_text(text):
    """Processes text: lowercase, remove punctuation, tokenize, filter stopwords."""
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    processed_words = [word for word in words if word not in STOPWORDS]
    return processed_words

def calculate_frequencies(words):
    """Calculates the frequency of each word."""
    return Counter(words)

def save_frequencies_to_csv(frequencies, csv_filepath):
    """Saves word frequencies to a CSV file."""
    try:
        with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Word', 'Frequency'])
            writer.writerows(frequencies.most_common())
        print(f"Word frequencies saved to {csv_filepath}")
    except Exception as e:
        print(f"Error writing CSV file {csv_filepath}: {e}")

def generate_and_save_wordcloud(frequencies, png_filepath):
    """Generates a word cloud and saves it as a PNG file."""
    try:
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(frequencies)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(png_filepath)
        plt.close()
        print(f"Word cloud image saved to {png_filepath}")
        return png_filepath
    except Exception as e:
        print(f"Error generating or saving word cloud image {png_filepath}: {e}")
        return None

def process_workflow(text_content, output_png, output_csv):
    """The core logic workflow."""
    processed_words = process_text(text_content)
    if not processed_words:
        print("No words found after processing.")
        return None, None

    word_frequencies = calculate_frequencies(processed_words)
    save_frequencies_to_csv(word_frequencies, output_csv)
    generate_and_save_wordcloud(word_frequencies, output_png)
    
    return output_png, output_csv

def run_cli(args):
    """Run the command line interface."""
    try:
        text_content = read_text_file(args.input_file)
        process_workflow(text_content, args.output_png, args.output_csv)
    except Exception as e:
        print(e)
        exit(1)

def launch_ui():
    """Launch the Gradio Web UI."""
    try:
        import gradio as gr
    except ImportError:
        print("Gradio is not installed. Please add it via `pixi add gradio`.")
        exit(1)

    def ui_handler(file_obj):
        if file_obj is None:
            return None, None
        
        try:
            with open(file_obj.name, 'r', encoding='utf-8') as f:
                text_content = f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return None, None
        
        output_png = os.path.abspath("output_wordcloud.png")
        output_csv = os.path.abspath("output_frequencies.csv")
        
        png_path, csv_path = process_workflow(text_content, output_png, output_csv)
        if png_path is None:
            return None, None
            
        return png_path, csv_path

    with gr.Blocks(title="WordCloud Generator") as interface:
        gr.Markdown("# Pythonic WordCloud Generator")
        gr.Markdown("Upload a transcript or text file to generate a word cloud and a frequency CSV.")
        
        with gr.Row():
            file_input = gr.File(label="Upload Text File", file_types=[".txt"])
            
        btn = gr.Button("Generate WordCloud")
        
        with gr.Row():
            image_output = gr.Image(label="Generated WordCloud", type="filepath")
            csv_output = gr.File(label="Word Frequencies CSV")
            
        btn.click(fn=ui_handler, inputs=[file_input], outputs=[image_output, csv_output])
        
    interface.launch()

def main():
    parser = argparse.ArgumentParser(description='Generate a word cloud from a text file.')
    parser.add_argument('input_file', nargs='?', help='Path to the input text file.')
    parser.add_argument('output_png', nargs='?', default='out.png', help='Path to save the output PNG image file.')
    parser.add_argument('output_csv', nargs='?', default='out.csv', help='Path to save the output CSV frequency file.')
    parser.add_argument('--ui', action='store_true', help='Launch the web user interface in the browser.')

    args = parser.parse_args()

    if args.ui:
        launch_ui()
    else:
        if not args.input_file:
            parser.error("input_file is required when not launching the UI (--ui)")
        run_cli(args)

if __name__ == "__main__":
    main()

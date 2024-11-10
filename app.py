# Importing necessary libraries
import json
import numpy as np
from sentence_transformers import SentenceTransformer, util
import gradio as gr

# Load your course data
with open("courses.json", "r") as f:
    courses = json.load(f)

# Initialize model for embedding generation
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embeddings for all course descriptions
course_descriptions = [course["description"] for course in courses]
course_embeddings = model.encode(course_descriptions, convert_to_tensor=True)

# Function to perform smart search
#def search_courses(query):
    # Generate embedding for the search query
    #query_embedding = model.encode(query, convert_to_tensor=True)

    # Compute cosine similarities between the query and all course descriptions
    #similarities = util.pytorch_cos_sim(query_embedding, course_embeddings)[0]

    # Find the top 5 most similar courses
    #top_results = np.argsort(similarities, descending=True)[:5]
    #top_results = np.argsort(-similarities)[:5]

    # Prepare output
    #results = []
    #for idx in top_results:
    #    course = courses[idx]
       # results.append({
            #"Title": course["title"],
            #"Description": course["description"],
            #"Link": course["link"]
        #})
    #return results
def search_courses(query):
    if not query.strip():
        return "Please enter a search query."
    
    # Convert query and titles to lowercase for case-insensitive matching
    query_lower = query.lower()
    title_matches = [course for course in courses if query_lower in course["title"].lower()]

    # If there are title matches, display those as results
    if title_matches:
        results = []
        for course in title_matches[:5]:  # Limit to top 5 title matches
            results.append({
                "Title": course["title"],
                "Description": course["description"],
                "Link": course["link"]
            })
        return results

    # Fallback to semantic search if no title matches are found
    query_embedding = model.encode(query, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(query_embedding, course_embeddings)[0]
    top_results = np.argsort(-similarities)[:5]  # Get top 5 most similar courses

    # Prepare output
    results = []
    for idx in top_results:
        course = courses[idx]
        results.append({
            "Title": course["title"],
            "Description": course["description"],
            "Link": course["link"]
        })
    return results

# Gradio Interface
def search_interface(query):
    # Call the search function and format results
    results = search_courses(query)
    display_text = "\n\n".join(
        [f"**Title**: {result['Title']}\n\n**Description**: {result['Description']}\n\n[Go to course]({result['Link']})" for result in results]
    )
    return display_text

# Creating the Gradio UI
iface = gr.Interface(
    fn=search_interface,
    inputs="text",
    outputs="markdown",
    title="Analytics Vidhya Free Courses - Smart Search",
    description="Enter a topic or keywords to find the most relevant free courses on Analytics Vidhya.",
    examples=["Machine Learning", "Data Science", "Python for Beginners"]
)

# Launch the Gradio interface
iface.launch()

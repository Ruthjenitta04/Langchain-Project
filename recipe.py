import cohere
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import streamlit as st

# Set your Cohere API key (Ensure this key is valid and not exposed publicly)
API_KEY = "J6WS1tyv8hy8uGEGGYKu0kecsgd4Tl62WnXl77bV"  # Replace with your actual Cohere API key
cohere_client = cohere.Client(API_KEY)

# Create a prompt template for generating food recipes
recipe_prompt = PromptTemplate(
    input_variables=["dish_name", "cuisine"],
    template="""You are a world-class chef. Generate a recipe for {dish_name}, a traditional dish from {cuisine}. 
    Include the ingredients and the detailed preparation steps. Make sure the recipe is easy to follow and 
    include the time needed to prepare and cook it."""
)

# Function to generate a recipe using Cohere
def generate_recipe(dish_name, cuisine):
    """
    Generates a recipe based on the dish name and cuisine type using Cohere.
    """
    try:
        # Format the prompt using LangChain's template
        formatted_prompt = recipe_prompt.format(dish_name=dish_name, cuisine=cuisine)

        # Generate the recipe using Cohere's API
        response = cohere_client.generate(
            model='command-xlarge-nightly',  # Use an updated model name
            prompt=formatted_prompt,
            max_tokens=300,  # Adjust max tokens based on your needs
            temperature=0.7  # Adjust temperature for more or less creativity
        )

        # Handle the response and check for generations
        if response.generations and len(response.generations) > 0:
            return response.generations[0].text.strip()  # Return the generated recipe
        else:
            return "No recipe was generated. Please try again with a different input."

    except Exception as e:
        # Handle any exceptions (e.g., API errors)
        return f"An error occurred: {str(e)}"

# Streamlit Interface
st.title("Food Recipe Generator")
st.write("Enter the name of a dish and the cuisine type to generate a detailed recipe.")

# Input fields for the user
dish_name = st.text_input("Dish Name", "Pasta")
cuisine = st.text_input("Cuisine", "Italian")

# Generate the recipe when the button is clicked
if st.button("Generate Recipe"):
    if dish_name and cuisine:
        recipe = generate_recipe(dish_name, cuisine)
        st.subheader(f"Recipe for {dish_name} ({cuisine} cuisine)")
        st.write(recipe)
    else:
        st.error("Please provide both a dish name and cuisine type.")

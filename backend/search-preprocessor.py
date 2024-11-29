from langchain_google_genai import ChatGoogleGenerativeAI as gemini
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from mediaDash_backend import get_scraping_instructions
import pandas as pd
import os

import json

def generate_search_queries(user_preferences):
    """
    Generate multiple search queries based on user preferences using Gemini AI.
    """
    llm = gemini(model="gemini-pro", temperature=0.7)
    
    prompt = PromptTemplate.from_template("""
    Based on the user's preferences, generate 3-4 different search queries that would help find relevant media content.
    Consider different aspects and combinations of their preferences.
    
    User preferences:
    Genre: {genre}
    Mood keywords: {mood_keywords}
    Previously enjoyed titles: {previous_titles}
    Subscriptions: {subscriptions}
    
    Return the queries as a JSON array of strings, each query optimized for finding relevant content.
    Focus on variety while maintaining relevance to the user's interests.
    """)
    
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.invoke(user_preferences)
    
    try:
        queries = json.loads(response.text)
        return queries if isinstance(queries, list) else []
    except json.JSONDecodeError:
        return []

def process_search_results(queries_results):
    """
    Process and combine results from multiple search queries.
    """
    llm = gemini(model="gemini-pro", temperature=0.7)
    
    prompt = PromptTemplate.from_template("""
    Analyze and combine the results from multiple search queries to provide a refined set of recommendations.
    Remove duplicates and rank the results based on relevance.
    
    Search Results from Multiple Queries:
    {queries_results}
    
    Previous Recommendations to Exclude:
    {previous_titles}
    
    Provide a consolidated list of the most relevant unique recommendations, excluding previously watched titles.
    Explain why each recommendation was selected and how it matches the user's preferences.
    """)
    
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.invoke({"queries_results": str(queries_results), "previous_titles": str(queries_results.get('previous_titles', []))})
    return response.text
def preprocess_search(user_data):
    """
    Main function to preprocess search using multiple AI-generated queries.
    """
    # generate multiple search queries w Gemini
    search_queries = generate_search_queries(user_data)
    res = []
    
    for query in search_queries:
        query_data = pd.DataFrame([{
            "search_query": query,
            "genre": user_data["genre"],
            "mood_keywords": user_data["mood_keywords"], 
            "previous_titles": user_data["previous_titles"],
            "subscriptions": user_data.get("subscriptions", "")
        }])
        
        temp_csv_path = "temp_query.csv"
        query_data.to_csv(temp_csv_path, index=False)
        scraped_data = get_scraping_instructions(temp_csv_path)
        res.append({"query": query, "results": scraped_data})
        os.remove(temp_csv_path)
    
    finalrec = process_search_results(res)
    return finalrec

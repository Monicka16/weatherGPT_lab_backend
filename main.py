import os
import sys
import logging
import requests
from contextlib import asynccontextmanager
from typing import Any, Optional

# Force root directory into sys.path for Vercel runtime resolution
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage

from weather_reference import (
    UV_INDEX_REFERENCE,
    WMO_CODE_REFERENCE,
    PRECIPITATION_RANGE_REFERENCE,
    VISIBILITY_RANGE_REFERENCE,
)

load_dotenv()
logger = logging.getLogger(__name__)

# Global variable to hold the initialized agent executor
agent_executor = None


# --- 1. Tool Definitions ---
@tool(description="Fetch Geolocation (latitude, longitude) for a given city name.")
def get_geolocation(city: str):
    """Fetch Geolocation (latitude, longitude) for a given city name."""
    url = os.environ.get("GEOLOCATION_API_EP", "https://geocoding-api.open-meteo.com/v1/search")
    geo_url = f"{url}?name={city}&count=1"
    try:
        geo_res = requests.get(geo_url).json()
        if not geo_res.get("results"):
            return f"Could not find coordinates for {city}."
        
        lat = geo_res["results"][0]["latitude"]
        lon = geo_res["results"][0]["longitude"]
        return (lat, lon)
    except Exception as e:
        return f"Error fetching coordinates: {e}"


@tool(description="Fetch the weather details for the given latitude and longitude.")
def get_weather(latitude: str, longitude: str):
    """Fetch the weather details for the given latitude and longitude."""
    url = os.environ.get("WEATHER_API_EP", "https://api.open-meteo.com/v1/forecast")
    weather_url = (
        f"{url}?latitude={latitude}&longitude={longitude}"
        "&daily=weather_code,sunrise,sunset,daylight_duration,sunshine_duration,moonset,moonrise,"
        "uv_index_max,apparent_temperature_min,apparent_temperature_max,temperature_2m_min,"
        "temperature_2m_max,rain_sum&hourly=temperature_2m,weather_code,wind_speed_10m,"
        "relative_humidity_2m,precipitation,pressure_msl,soil_temperature_0cm,soil_temperature_6cm,"
        "visibility,wind_speed_80m,wind_direction_10m,wind_direction_80m,apparent_temperature,"
        "soil_temperature_18cm,uv_index,is_day,sunshine_duration&models=best_match&forecast_days=14"
    )
    try:
        return requests.get(weather_url).json()
    except Exception as e:
        return f"Error fetching weather details: {e}"


# --- 2. FastAPI Lifespan Handler ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    global agent_executor
    
    # Environment Check
    if not os.environ.get("GOOGLE_API_KEY"):
        raise RuntimeError("GOOGLE_API_KEY is missing from environment variables.")
    
    model_name = os.environ.get("MODEL", "gemini-1.5-flash")
    
    # Initialize LLM & Agent
    llm = ChatGoogleGenerativeAI(model=model_name)
    tools = [get_geolocation, get_weather]

    system_prompt = SystemMessage(
        """You are a weather expert with access to 2 tools.
    Use get_geolocation() to get the geolocation for a city mentioned in the user prompt.
    Use get_weather() to get the weather details from the tool. It returns data in JSON format.
    If the city is not given, use the geolocation directly from the user prompt.
    
    CRITICAL FORMATTING INSTRUCTION:
    You MUST ALWAYS structure your final response strictly into these 3 sections in order:

    ### Weather Details
    - List relevant metrics (Temperature, Precipitation, Visibility, Wind, UV Index, Time of Day).

    ### Verdict
    - Give a direct, clear answer to the user's question (e.g., "Yes, conditions are great for football tonight.").

    ### Advice
    - Provide actionable recommendation tailored to the activity or persona (e.g., clothing, timing, precautions).

    Never output raw JSON keys like is_day. Translate is_day: 0 to Nighttime and is_day: 1 to Daytime.
    Do not use LLM internal knowledge for weather—always use the provided tools.
    """
    )

    agent_executor = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt
    )
    
    yield


# --- 3. App Initialization & Schemas ---
app = FastAPI(
    title="WeatherGPT Backend",
    description="A chat service powered by LangChain and Google Gemini.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    conversation_id: str = Field(..., min_length=1, example="user1-session1")
    message: str = Field(..., example="can i play football outside now?")
    latitude: Optional[float] = Field(None, example=12.9716)
    longitude: Optional[float] = Field(None, example=77.5946)
    city_name: Optional[str] = Field(None, example="Bengaluru")

class ChatResponse(BaseModel):
    reply: str


# --- 4. Helper Function ---
def extract_text(content: Any) -> str:
    """Helper to extract raw text content safely from string or list-of-dicts outputs."""
    if isinstance(content, str):
        return content
    elif isinstance(content, list) and len(content) > 0:
        if isinstance(content[0], dict) and "text" in content[0]:
            return content[0]["text"]
        return str(content[0])
    return str(content)


# --- 5. Endpoints ---
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not agent_executor:
        raise HTTPException(status_code=500, detail="Agent is not initialized.")
    
    try:
        prompt_message = request.message
        
        # Inject location coordinates/context if available and not explicitly mentioned
        if request.latitude is not None and request.longitude is not None:
            location_ctx = f" (User's current coordinates: latitude={request.latitude}, longitude={request.longitude}"
            if request.city_name:
                location_ctx += f", city={request.city_name}"
            location_ctx += ")"
            prompt_message += location_ctx

        response = await agent_executor.ainvoke({
            "messages": [("user", prompt_message)]
        })
        
        last_message = response["messages"][-1]
        text_output = extract_text(last_message.content)
        
        return ChatResponse(reply=text_output)
    
    except Exception as e:
        logger.error(f"Error processing chat request for {request.conversation_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="An error occurred while processing your request. Please try again."
        )

@app.get("/health")
async def health_check():
    return {"status": "ok", "agent_ready": agent_executor is not None}
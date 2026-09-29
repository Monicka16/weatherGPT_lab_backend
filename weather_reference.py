import json

UV_INDEX_REFERENCE = {
  "uv_scale": {
    "0-2": {
      "level": "Low",
      "color": "Green",
      "risk": "Minimal danger"
    },
    "3-5": {
      "level": "Moderate",
      "color": "Yellow",
      "risk": "Low to moderate risk"
    },
    "6-7": {
      "level": "High",
      "color": "Orange",
      "risk": "High risk of harm"
    },
    "8-10": {
      "level": "Very High",
      "color": "Red",
      "risk": "Very high risk of damage"
    },
    "11+": {
      "level": "Extreme",
      "color": "Violet",
      "risk": "Extreme risk of harm"
    }
  },
  "discrete_lookup": {
    "0": "Low",
    "1": "Low",
    "2": "Low",
    "3": "Moderate",
    "4": "Moderate",
    "5": "Moderate",
    "6": "High",
    "7": "High",
    "8": "Very High",
    "9": "Very High",
    "10": "Very High",
    "11+": "Extreme"
  }
}

PRECIPITATION_RANGE_REFERENCE = {
  "title": "Meteorological Precipitation Intensity Classification",
  "unit": "mm/hr",
  "classifications": [
    {
      "condition": "No Precipitation",
      "min_mm_per_hour": 0.0,
      "max_mm_per_hour": 0.0,
      "description": "Dry conditions; no measurable precipitation."
    },
    {
      "condition": "Trace / Very Light",
      "min_mm_per_hour": 0.01,
      "max_mm_per_hour": 0.25,
      "description": "Barely measurable precipitation droplets; no accumulation."
    },
    {
      "condition": "Light Rain",
      "min_mm_per_hour": 0.25,
      "max_mm_per_hour": 2.5,
      "description": "Light drizzle or light rain; slow puddle formation."
    },
    {
      "condition": "Moderate Rain",
      "min_mm_per_hour": 2.5,
      "max_mm_per_hour": 7.6,
      "description": "Continuous steady rainfall; umbrellas required, puddles forming."
    },
    {
      "condition": "Heavy Rain",
      "min_mm_per_hour": 7.6,
      "max_mm_per_hour": 50.0,
      "description": "Heavy downpour; rapid accumulation, reduced visibility while driving."
    },
    {
      "condition": "Violent / Torrential Rain",
      "min_mm_per_hour": 50.0,
      "max_mm_per_hour": 100.0,
      "description": "Extreme convective rainfall; high risk of flash flooding and hydroplaning."
    }
  ]
}

WMO_CODE_REFERENCE = [
  {
    "code": "00",
    "description": "Cloud development not observed or not observable"
  },
  {
    "code": "01",
    "description": "Clouds generally dissolving or becoming less developed"
  },
  {
    "code": "02",
    "description": "State of sky on the whole unchanged"
  },
  {
    "code": "03",
    "description": "Clouds generally forming or developing"
  },
  {
    "code": "04",
    "description": "Visibility reduced by smoke, e.g. veldt or forest fires, industrial smoke or volcanic ashes"
  },
  {
    "code": "05",
    "description": "Haze"
  },
  {
    "code": "06",
    "description": "Widespread dust in suspension in the air, not raised by wind at or near the station at the time of observation"
  },
  {
    "code": "07",
    "description": "Dust or sand raised by wind at or near the station at the time of observation, but no well developed dust whirl(s) or sand whirl(s), and no duststorm or sandstorm seen"
  },
  {
    "code": "08",
    "description": "Well developed dust whirl(s) or sand whirl(s) seen at or near the station during the preceding hour or at the time ot observation, but no duststorm or sandstorm"
  },
  {
    "code": "09",
    "description": "Duststorm or sandstorm within sight at the time of observation, or at the station during the preceding hour"
  },
  {
    "code": "10",
    "description": "Mist"
  },
  {
    "code": "11",
    "description": "Patches shallow fog or ice fog at the station, whether on land or sea, not deeper than about 2 metres on land or 10 metres at sea"
  },
  {
    "code": "12",
    "description": "More or less continuous"
  },
  {
    "code": "13",
    "description": "Lightning visible, no thunder heard"
  },
  {
    "code": "14",
    "description": "Precipitation within sight, not reaching the ground or the surface of the sea"
  },
  {
    "code": "15",
    "description": "Precipitation within sight, reaching the ground or the surface of the sea, but distant, i.e. estimated to be more than 5 km from the station"
  },
  {
    "code": "16",
    "description": "Precipitation within sight, reaching the ground or the surface of the sea, near to, but not at the station"
  },
  {
    "code": "17",
    "description": "Thunderstorm, but no precipitation at the time of observation"
  },
  {
    "code": "18",
    "description": "Squalls at or within sight of the station during the preceding hour or at the time of observation"
  },
  {
    "code": "19",
    "description": "Funnel cloud(s)"
  },
  {
    "code": "20",
    "description": "Drizzle (not freezing) or snow grains not falling as shower(s)"
  },
  {
    "code": "21",
    "description": "Rain (not freezing)"
  },
  {
    "code": "22",
    "description": "Snow"
  },
  {
    "code": "23",
    "description": "Rain and snow or ice pellets"
  },
  {
    "code": "24",
    "description": "Freezing drizzle or freezing rain"
  },
  {
    "code": "25",
    "description": "Shower(s) of rain"
  },
  {
    "code": "26",
    "description": "Shower(s) of snow, or of rain and snow"
  },
  {
    "code": "27",
    "description": "Shower(s) of hail, or of rain and hail"
  },
  {
    "code": "28",
    "description": "Fog or ice fog"
  },
  {
    "code": "29",
    "description": "Thunderstorm (with or without precipitation)"
  },
  {
    "code": "30",
    "description": "Slight or moderate duststorm or sandstorm - has decreased during the preceding hour"
  },
  {
    "code": "31",
    "description": "Slight or moderate duststorm or sandstorm - no appreciable change during the preceding hour"
  },
  {
    "code": "32",
    "description": "Slight or moderate duststorm or sandstorm - has begun or has increased during the preceding hour"
  },
  {
    "code": "33",
    "description": "Severe duststorm or sandstorm - has decreased during the preceding hour"
  },
  {
    "code": "34",
    "description": "Severe duststorm or sandstorm - no appreciable change during the preceding hour"
  },
  {
    "code": "35",
    "description": "Severe duststorm or sandstorm - has begun or has increased during the preceding hour"
  },
  {
    "code": "36",
    "description": "Slight or moderate blowing snow generally low (below eye level)"
  },
  {
    "code": "37",
    "description": "Heavy drifting snow"
  },
  {
    "code": "38",
    "description": "Slight or moderate blowing snow generally high (above eye level)"
  },
  {
    "code": "39",
    "description": "Heavy drifting snow"
  },
  {
    "code": "40",
    "description": "Fog or ice fog at a distance at the time of observation, but not at the station during the preceding hour, the fog or ice fog extending to a level above that of the observer"
  },
  {
    "code": "41",
    "description": "Fog or ice fog in patches"
  },
  {
    "code": "42",
    "description": "Fog or ice fog, sky visible has become thinner during the preceding hour"
  },
  {
    "code": "43",
    "description": "Fog or ice fog, sky invisible"
  },
  {
    "code": "44",
    "description": "Fog or ice fog, sky visible no appreciable change during the preceding hour"
  },
  {
    "code": "45",
    "description": "Fog or ice fog, sky invisible"
  },
  {
    "code": "46",
    "description": "Fog or ice fog, sky visible has begun or has become thicker during the preceding hour"
  },
  {
    "code": "47",
    "description": "Fog or ice fog, sky invisible"
  },
  {
    "code": "48",
    "description": "Fog, depositing rime, sky visible"
  },
  {
    "code": "49",
    "description": "Fog, depositing rime, sky invisible"
  },
  {
    "code": "50",
    "description": "Drizzle, not freezing, intermittent slight at time of observation"
  },
  {
    "code": "51",
    "description": "Drizzle, not freezing, continuous"
  },
  {
    "code": "52",
    "description": "Drizzle, not freezing, intermittent moderate at time of observation"
  },
  {
    "code": "53",
    "description": "Drizzle, not freezing, continuous"
  },
  {
    "code": "54",
    "description": "Drizzle, not freezing, intermittent heavy (dense) at time of observation"
  },
  {
    "code": "55",
    "description": "Drizzle, not freezing, continuous"
  },
  {
    "code": "56",
    "description": "Drizzle, freezing, slight"
  },
  {
    "code": "57",
    "description": "Drizzle, freezing, moderate or heavy (dence)"
  },
  {
    "code": "58",
    "description": "Drizzle and rain, slight"
  },
  {
    "code": "59",
    "description": "Drizzle and rain, moderate or heavy"
  },
  {
    "code": "60",
    "description": "Rain, not freezing, intermittent slight at time of observation"
  },
  {
    "code": "61",
    "description": "Rain, not freezing, continuous"
  },
  {
    "code": "62",
    "description": "Rain, not freezing, intermittent moderate at time of observation"
  },
  {
    "code": "63",
    "description": "Rain, not freezing, continuous"
  },
  {
    "code": "64",
    "description": "Rain, not freezing, intermittent heavy at time of observation"
  },
  {
    "code": "65",
    "description": "Rain, not freezing, continuous"
  },
  {
    "code": "66",
    "description": "Rain, freezing, slight"
  },
  {
    "code": "67",
    "description": "Rain, freezing, moderate or heavy (dence)"
  },
  {
    "code": "68",
    "description": "Rain or drizzle and snow, slight"
  },
  {
    "code": "69",
    "description": "Rain or drizzle and snow, moderate or heavy"
  },
  {
    "code": "70",
    "description": "Intermittent fall of snowflakes slight at time of observation"
  },
  {
    "code": "71",
    "description": "Continuous fall of snowflakes"
  },
  {
    "code": "72",
    "description": "Intermittent fall of snowflakes moderate at time of observation"
  },
  {
    "code": "73",
    "description": "Continuous fall of snowflakes"
  },
  {
    "code": "74",
    "description": "Intermittent fall of snowflakes heavy at time of observation"
  },
  {
    "code": "75",
    "description": "Continuous fall of snowflakes"
  },
  {
    "code": "76",
    "description": "Diamond dust (with or without fog)"
  },
  {
    "code": "77",
    "description": "Snow grains (with or without fog)"
  },
  {
    "code": "78",
    "description": "Isolated star-like snow crystals (with or without fog)"
  },
  {
    "code": "79",
    "description": "Ice pellets"
  },
  {
    "code": "80",
    "description": "Rain shower(s), slight"
  },
  {
    "code": "81",
    "description": "Rain shower(s), moderate or heavy"
  },
  {
    "code": "82",
    "description": "Rain shower(s), violent"
  },
  {
    "code": "83",
    "description": "Shower(s) of rain and snow mixed, slight"
  },
  {
    "code": "84",
    "description": "Shower(s) of rain and snow mixed, moderate or heavy"
  },
  {
    "code": "85",
    "description": "Snow shower(s), slight"
  },
  {
    "code": "86",
    "description": "Snow shower(s), moderate or heavy"
  },
  {
    "code": "87",
    "description": "Shower(s) of snow pellets or small hail, with or without rain or rain and snow mixed - slight"
  },
  {
    "code": "88",
    "description": "- moderate or heavy"
  },
  {
    "code": "89",
    "description": "Shower(s) of hail, with or without rain or rain and snow mixed, not associated with thunder - slight"
  },
  {
    "code": "90",
    "description": "- moderate or heavy"
  },
  {
    "code": "91",
    "description": "Slight rain at time of observation Thunderstorm during the preceding hour but not at time of observation"
  },
  {
    "code": "92",
    "description": "Moderate or heavy rain at time of observation"
  },
  {
    "code": "93",
    "description": "Slight snow, or rain and snow mixed or hail at time of observation"
  },
  {
    "code": "94",
    "description": "Moderate or heavy snow, or rain and snow mixed or hail at time of observation"
  },
  {
    "code": "95",
    "description": "Thunderstorm, slight or moderate, without hail but with rain and/or snow at time of observation Thunderstorm at time of observation"
  },
  {
    "code": "96",
    "description": "Thunderstorm, slight or moderate, with hail at time of observation"
  },
  {
    "code": "97",
    "description": "Thunderstorm, heavy, without hail but with rain and/or snow at time of observation"
  },
  {
    "code": "98",
    "description": "Thunderstorm combined with duststorm or sandstorm at time of observation"
  },
  {
    "code": "99",
    "description": "Thunderstorm, heavy, with hail at time of observation"
  }
]

VISIBILITY_RANGE_REFERENCE=""
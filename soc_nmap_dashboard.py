#!/usr/bin/env python3
"""
DSTERMINAL SOC-GRADE NMAP SCAN DASHBOARD - COMPLETE EDITION
Hacker-style 3-Panel Layout | Real-time Scan Monitoring | AI Vulnerability Scoring
"""

import os
import sys
import time
import json
import re
import shutil
import subprocess
import threading
import webbrowser
import random
import math
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field

# ============================================================
# ANSI COLORS - HACKER THEME
# ============================================================

class Colors:
    GREEN = '\033[92m'
    DARK_GREEN = '\033[32m'
    BRIGHT_GREEN = '\033[92m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    MAGENTA = '\033[95m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    WHITE = '\033[97m'
    ORANGE = '\033[38;5;208m'
    PINK = '\033[38;5;205m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    # Use this instead of DIM (some terminals don't support DIM)
    DIM = '\033[2m' if hasattr('\033[2m', '__str__') else '\033[90m'  # Fallback to dark gray


# ============================================================
# Required Imports
# ============================================================

try:
    import folium
    from folium.plugins import HeatMap
    GEO_AVAILABLE = True
except ImportError:
    GEO_AVAILABLE = False

try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


# ============================================================
# ORGANIZATION LOCATION DATABASE (Universal - Works for ANY Country)
# ============================================================

class OrganizationLocationDB:
    """Database of organization headquarters locations (not server locations)"""
    
    # Add organizations from ANY country here
    ORGANIZATIONS = {
        # ========== MALAWI ==========
        "unima.ac.mw": {"country": "Malawi", "city": "Zomba", "lat": -15.3833, "lon": 35.3167, "flag": "🇲🇼", "region": "East Africa"},
        "must.ac.mw": {"country": "Malawi", "city": "Blantyre", "lat": -15.7833, "lon": 34.9667, "flag": "🇲🇼", "region": "East Africa"},
        "sparcsystems.africa": {"country": "Malawi", "city": "Blantyre", "lat": -15.7833, "lon": 34.9667, "flag": "🇲🇼", "region": "East Africa"},
        "poly.ac.mw": {"country": "Malawi", "city": "Blantyre", "lat": -15.7833, "lon": 34.9667, "flag": "🇲🇼", "region": "East Africa"},
        "kuhes.ac.mw": {"country": "Malawi", "city": "Lilongwe", "lat": -13.9833, "lon": 33.7833, "flag": "🇲🇼", "region": "East Africa"},
        "mzuni.ac.mw": {"country": "Malawi", "city": "Mzuzu", "lat": -11.4667, "lon": 34.0167, "flag": "🇲🇼", "region": "East Africa"},
        "cc.ac.mw": {"country": "Malawi", "city": "Blantyre", "lat": -15.7833, "lon": 34.9667, "flag": "🇲🇼", "region": "East Africa"},
        "medcol.ac.mw": {"country": "Malawi", "city": "Blantyre", "lat": -15.7833, "lon": 34.9667, "flag": "🇲🇼", "region": "East Africa"},
        
        # ========== SOUTH AFRICA ==========
        "uct.ac.za": {"country": "South Africa", "city": "Cape Town", "lat": -33.9249, "lon": 18.4241, "flag": "🇿🇦", "region": "Southern Africa"},
        "up.ac.za": {"country": "South Africa", "city": "Pretoria", "lat": -25.7548, "lon": 28.2315, "flag": "🇿🇦", "region": "Southern Africa"},
        "uj.ac.za": {"country": "South Africa", "city": "Johannesburg", "lat": -26.2041, "lon": 28.0473, "flag": "🇿🇦", "region": "Southern Africa"},
        "wits.ac.za": {"country": "South Africa", "city": "Johannesburg", "lat": -26.1929, "lon": 28.0305, "flag": "🇿🇦", "region": "Southern Africa"},
        "stel.ac.za": {"country": "South Africa", "city": "Stellenbosch", "lat": -33.9328, "lon": 18.8644, "flag": "🇿🇦", "region": "Southern Africa"},
        "nmmu.ac.za": {"country": "South Africa", "city": "Gqeberha", "lat": -33.9618, "lon": 25.6099, "flag": "🇿🇦", "region": "Southern Africa"},
        "dut.ac.za": {"country": "South Africa", "city": "Durban", "lat": -29.8587, "lon": 31.0218, "flag": "🇿🇦", "region": "Southern Africa"},
        "tut.ac.za": {"country": "South Africa", "city": "Pretoria", "lat": -25.7548, "lon": 28.2315, "flag": "🇿🇦", "region": "Southern Africa"},
        
        # ========== KENYA ==========
        "uonbi.ac.ke": {"country": "Kenya", "city": "Nairobi", "lat": -1.2921, "lon": 36.8219, "flag": "🇰🇪", "region": "East Africa"},
        "ku.ac.ke": {"country": "Kenya", "city": "Nairobi", "lat": -1.2225, "lon": 36.8966, "flag": "🇰🇪", "region": "East Africa"},
        "tukenya.ac.ke": {"country": "Kenya", "city": "Nairobi", "lat": -1.3204, "lon": 36.8157, "flag": "🇰🇪", "region": "East Africa"},
        "mku.ac.ke": {"country": "Kenya", "city": "Thika", "lat": -1.0386, "lon": 37.0908, "flag": "🇰🇪", "region": "East Africa"},
        "daystar.ac.ke": {"country": "Kenya", "city": "Nairobi", "lat": -1.2921, "lon": 36.8219, "flag": "🇰🇪", "region": "East Africa"},
        
        # ========== NIGERIA ==========
        "unilag.edu.ng": {"country": "Nigeria", "city": "Lagos", "lat": 6.5170, "lon": 3.3968, "flag": "🇳🇬", "region": "West Africa"},
        "unn.edu.ng": {"country": "Nigeria", "city": "Nsukka", "lat": 6.8575, "lon": 7.3981, "flag": "🇳🇬", "region": "West Africa"},
        "oauife.edu.ng": {"country": "Nigeria", "city": "Ile-Ife", "lat": 7.5000, "lon": 4.5000, "flag": "🇳🇬", "region": "West Africa"},
        "abu.edu.ng": {"country": "Nigeria", "city": "Zaria", "lat": 11.1667, "lon": 7.6167, "flag": "🇳🇬", "region": "West Africa"},
        "uniben.edu": {"country": "Nigeria", "city": "Benin City", "lat": 6.3176, "lon": 5.6145, "flag": "🇳🇬", "region": "West Africa"},
        
        # ========== GHANA ==========
        "ug.edu.gh": {"country": "Ghana", "city": "Accra", "lat": 5.6500, "lon": -0.1868, "flag": "🇬🇭", "region": "West Africa"},
        "knust.edu.gh": {"country": "Ghana", "city": "Kumasi", "lat": 6.6750, "lon": -1.5714, "flag": "🇬🇭", "region": "West Africa"},
        "central.edu.gh": {"country": "Ghana", "city": "Accra", "lat": 5.6500, "lon": -0.1868, "flag": "🇬🇭", "region": "West Africa"},
        
        # ========== EGYPT ==========
        "cu.edu.eg": {"country": "Egypt", "city": "Cairo", "lat": 30.0333, "lon": 31.2333, "flag": "🇪🇬", "region": "North Africa"},
        "alexu.edu.eg": {"country": "Egypt", "city": "Alexandria", "lat": 31.2001, "lon": 29.9187, "flag": "🇪🇬", "region": "North Africa"},
        
        # ========== USA ==========
        "harvard.edu": {"country": "USA", "city": "Cambridge", "lat": 42.3744, "lon": -71.1169, "flag": "🇺🇸", "region": "North America"},
        "stanford.edu": {"country": "USA", "city": "Stanford", "lat": 37.4275, "lon": -122.1697, "flag": "🇺🇸", "region": "North America"},
        "mit.edu": {"country": "USA", "city": "Cambridge", "lat": 42.3601, "lon": -71.0942, "flag": "🇺🇸", "region": "North America"},
        
        # ========== UK ==========
        "ox.ac.uk": {"country": "United Kingdom", "city": "Oxford", "lat": 51.7520, "lon": -1.2577, "flag": "🇬🇧", "region": "Europe"},
        "cam.ac.uk": {"country": "United Kingdom", "city": "Cambridge", "lat": 52.2053, "lon": 0.1218, "flag": "🇬🇧", "region": "Europe"},
        
        # ========== GERMANY ==========
        "tu-berlin.de": {"country": "Germany", "city": "Berlin", "lat": 52.5200, "lon": 13.4050, "flag": "🇩🇪", "region": "Europe"},
        "lmu.de": {"country": "Germany", "city": "Munich", "lat": 48.1351, "lon": 11.5820, "flag": "🇩🇪", "region": "Europe"},
        
        # ========== INDIA ==========
        "iitb.ac.in": {"country": "India", "city": "Mumbai", "lat": 19.0760, "lon": 72.8777, "flag": "🇮🇳", "region": "South Asia"},
        "iisc.ac.in": {"country": "India", "city": "Bengaluru", "lat": 12.9716, "lon": 77.5946, "flag": "🇮🇳", "region": "South Asia"},
    }
    
    @classmethod
    def get_organization_location(cls, domain: str, hostname: str = "") -> Optional[Dict]:
        """Get organization headquarters location for a domain"""
        domain_lower = domain.lower()
        hostname_lower = hostname.lower()
        
        # Check exact domain match
        if domain_lower in cls.ORGANIZATIONS:
            return cls.ORGANIZATIONS[domain_lower]
        
        # Check partial match (e.g., .ac.mw domains)
        for org_domain, location in cls.ORGANIZATIONS.items():
            if org_domain in domain_lower or domain_lower.endswith(org_domain):
                return location
        
        # Check if it's an .africa domain (could be any African country)
        if domain_lower.endswith('.africa') or '.africa' in domain_lower:
            return {
                "country": "Africa (HQ Unknown)",
                "city": "Unknown",
                "lat": 0,
                "lon": 0,
                "flag": "🌍",
                "region": "Africa",
                "note": "Organization headquarters location unknown - showing approximate continent"
            }
        
        return None
    
    @classmethod
    def add_organization(cls, domain: str, country: str, city: str, lat: float, lon: float, flag: str = "🌐", region: str = "Unknown"):
        """Dynamically add an organization to the database"""
        cls.ORGANIZATIONS[domain.lower()] = {
            "country": country,
            "city": city,
            "lat": lat,
            "lon": lon,
            "flag": flag,
            "region": region
        }
        print(f"[+] Added {domain} to organization database ({country})")


# Initialize organization database at startup

# ============================================================
# Data Classes
# ============================================================

@dataclass
class NetworkNode:
    ip: str
    hostname: str = ""
    country: str = ""
    city: str = ""
    lat: float = 0.0
    lon: float = 0.0
    isp: str = ""
    ports: List[Dict] = field(default_factory=list)
    risk_score: float = 0.0
    is_organization_location: bool = False
    server_location: str = ""


@dataclass
class ScanHistory:
    timestamp: datetime
    target: str
    duration: float
    open_ports: int
    risk_score: float
    services: List[str]


# ============================================================
# AI Vulnerability Scorer
# ============================================================

class AIVulnerabilityScorer:
    @staticmethod
    def analyze_service(service: str, port: str, version: str = "") -> Dict:
        vuln_db = {
            "ftp": {"cvss_id": "CVE-2024-1234", "score": 7.5, "exploit": "Metasploit/ftp"},
            "ssh": {"cvss_id": "CVE-2024-5678", "score": 5.5, "exploit": "Hydra/SSH"},
            "telnet": {"cvss_id": "CVE-2024-9012", "score": 9.0, "exploit": "TelnetBleed"},
            "http": {"cvss_id": "CVE-2024-3456", "score": 6.5, "exploit": "SQLMap/HTTP"},
            "https": {"cvss_id": "CVE-2024-7890", "score": 5.0, "exploit": "Heartbleed"},
            "smb": {"cvss_id": "CVE-2024-2345", "score": 8.5, "exploit": "EternalBlue"},
            "rdp": {"cvss_id": "CVE-2024-6789", "score": 9.0, "exploit": "BlueKeep"},
            "domain": {"cvss_id": "CVE-2024-1111", "score": 6.0, "exploit": "DNSpoof"},
            "rtsp": {"cvss_id": "CVE-2024-3333", "score": 6.0, "exploit": "RTSP Brute"},
            "dns": {"cvss_id": "CVE-2024-5555", "score": 7.0, "exploit": "DNS Cache Poisoning"},
        }
        
        service_lower = service.lower()
        for vuln_service, data in vuln_db.items():
            if vuln_service in service_lower:
                severity = "CRITICAL" if data["score"] >= 9 else "HIGH" if data["score"] >= 7 else "MEDIUM"
                return {
                    "vulnerable": True,
                    "cvss_id": data["cvss_id"],
                    "cvss_score": data["score"],
                    "severity": severity,
                    "exploit": data["exploit"],
                    "recommendation": f"Patch {service} immediately" if data["score"] >= 7 else f"Update {service}"
                }
        
        return {"vulnerable": False, "cvss_score": 0, "severity": "LOW", "recommendation": "Monitor"}


# ============================================================
# Enhanced GeoIP Lookup with Organization Location
# ============================================================

def get_server_location(ip: str) -> Dict:
    """Get actual server location (where the website is hosted)"""
    try:
        if ip.startswith(("192.168.", "10.", "172.", "127.", "169.254.")):
            return {"country": "Private Network", "city": "Local", "lat": 0, "lon": 0, "isp": "Private", "location": "Local Network"}
        
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        data = response.json()
        return {
            "country": data.get("country", "Unknown"),
            "city": data.get("city", "Unknown"),
            "lat": data.get("lat", 0),
            "lon": data.get("lon", 0),
            "isp": data.get("isp", "Unknown"),
            "location": f"{data.get('city', 'Unknown')}, {data.get('country', 'Unknown')}",
            "is_organization_location": False
        }
    except:
        return {"country": "Unknown", "city": "Unknown", "lat": 0, "lon": 0, "isp": "Unknown", "location": "Unknown"}


def enhanced_geoip_lookup(domain: str, ip: str) -> Tuple[Dict, bool]:
    """
    Enhanced GeoIP that shows ORGANIZATION location, not server location
    Returns (location_dict, is_organization_location)
    """
    # First, check if we have the organization's headquarters location
    org_location = OrganizationLocationDB.get_organization_location(domain, ip)
    
    if org_location and org_location.get("lat", 0) != 0:
        # Get server location for comparison (CDN/cloud info)
        server_loc = get_server_location(ip)
        
        return {
            "country": org_location["country"],
            "city": org_location["city"],
            "lat": org_location["lat"],
            "lon": org_location["lon"],
            "flag": org_location.get("flag", "🌐"),
            "region": org_location.get("region", "Unknown"),
            "is_organization_location": True,
            "server_location": server_loc.get("location", "Unknown"),
            "server_country": server_loc.get("country", "Unknown"),
            "note": f"Showing organization headquarters in {org_location['country']}"
        }, True
    
    # Fallback to server location
    server_loc = get_server_location(ip)
    return server_loc, False


class EnhancedGeoMapVisualizer:
    """Advanced Geographic Threat Intelligence Map with Blinking Markers and Organization Locations"""
    
    def __init__(self):
        self.locations = []
        
    def add_location(self, lat: float, lon: float, ip: str, risk_score: float, 
                     ports: List[Dict] = None, country: str = "", 
                     is_org_location: bool = False, server_location: str = "",
                     domain: str = ""):
        self.locations.append({
            "lat": lat, "lon": lon, "ip": ip, "risk_score": risk_score,
            "ports": ports or [], "country": country, "timestamp": datetime.now(),
            "is_organization_location": is_org_location,
            "server_location": server_location,
            "domain": domain
        })
    
    def generate_threat_map(self) -> str:
        """Generate interactive threat intelligence map with BLINKING lines and circles"""
        if not GEO_AVAILABLE:
            return '<div style="padding:50px;text-align:center;">🌍 GeoIP module not available</div>'
        
        m = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB dark_matter', control_scale=True)
        
        # CSS for blinking animations - LINES AND CIRCLES
        blink_css = """
        <style>
            /* Blinking animations for circles */
            @keyframes blink-red { 
                0%, 100% { opacity: 1; filter: drop-shadow(0 0 5px #ff0000); transform: scale(1); } 
                50% { opacity: 0.3; filter: drop-shadow(0 0 20px #ff0000); transform: scale(1.2); } 
            }
            @keyframes blink-orange { 
                0%, 100% { opacity: 1; filter: drop-shadow(0 0 5px #ff6600); transform: scale(1); } 
                50% { opacity: 0.4; filter: drop-shadow(0 0 15px #ff6600); transform: scale(1.15); } 
            }
            @keyframes blink-yellow { 
                0%, 100% { opacity: 1; filter: drop-shadow(0 0 5px #ffcc00); transform: scale(1); } 
                50% { opacity: 0.5; filter: drop-shadow(0 0 10px #ffcc00); transform: scale(1.1); } 
            }
            @keyframes blink-green { 
                0%, 100% { opacity: 1; filter: drop-shadow(0 0 5px #00ff00); transform: scale(1); } 
                50% { opacity: 0.6; filter: drop-shadow(0 0 8px #00ff00); transform: scale(1.05); } 
            }
            
            /* Blinking animations for lines */
            @keyframes blink-line-red {
                0%, 100% { stroke: #ff0000; stroke-width: 2; stroke-dasharray: 5, 5; opacity: 1; }
                50% { stroke: #ff6666; stroke-width: 4; stroke-dasharray: 10, 5; opacity: 0.7; }
            }
            @keyframes blink-line-orange {
                0%, 100% { stroke: #ff6600; stroke-width: 2; stroke-dasharray: 5, 5; opacity: 1; }
                50% { stroke: #ffaa66; stroke-width: 3; stroke-dasharray: 8, 5; opacity: 0.7; }
            }
            @keyframes blink-line-yellow {
                0%, 100% { stroke: #ffcc00; stroke-width: 2; stroke-dasharray: 5, 5; opacity: 1; }
                50% { stroke: #ffeeaa; stroke-width: 3; stroke-dasharray: 6, 5; opacity: 0.7; }
            }
            @keyframes blink-line-green {
                0%, 100% { stroke: #00ff00; stroke-width: 1.5; stroke-dasharray: 4, 4; opacity: 1; }
                50% { stroke: #88ff88; stroke-width: 2.5; stroke-dasharray: 6, 4; opacity: 0.7; }
            }
            
            /* Circle blinking classes */
            .blink-critical { animation: blink-red 0.6s ease-in-out infinite; }
            .blink-high { animation: blink-orange 0.8s ease-in-out infinite; }
            .blink-medium { animation: blink-yellow 1s ease-in-out infinite; }
            .blink-low { animation: blink-green 1.2s ease-in-out infinite; }
            
            /* Line blinking classes */
            .line-critical { animation: blink-line-red 0.6s ease-in-out infinite; }
            .line-high { animation: blink-line-orange 0.8s ease-in-out infinite; }
            .line-medium { animation: blink-line-yellow 1s ease-in-out infinite; }
            .line-low { animation: blink-line-green 1.2s ease-in-out infinite; }
            
            /* Pulse ring effect */
            @keyframes pulse-ring {
                0% { transform: scale(0.8); opacity: 0.8; }
                100% { transform: scale(2); opacity: 0; }
            }
            .pulse-ring {
                animation: pulse-ring 1.5s ease-out infinite;
            }
            
            .live-badge { 
                position: fixed; top: 10px; right: 10px; background: #00ff00; color: #000; 
                padding: 5px 10px; border-radius: 5px; font-family: monospace; font-size: 10px; 
                z-index: 1000; animation: blink-green 1s infinite; font-weight: bold;
            }
            
            .org-marker {
                border: 3px solid #ffaa00;
                box-shadow: 0 0 10px rgba(255,170,0,0.5);
            }
            
            /* Animated connection line */
            .animated-line {
                stroke-dasharray: 10;
                animation: dash 1s linear infinite;
            }
            @keyframes dash {
                to { stroke-dashoffset: -20; }
            }
        </style>
        """
        m.get_root().header.add_child(folium.Element(blink_css))
        m.get_root().html.add_child(folium.Element('<div class="live-badge">🔴 LIVE MONITORING ACTIVE 🔴</div>'))
        
        # Heatmap
        heat_data = [[loc["lat"], loc["lon"], loc["risk_score"] / 10] for loc in self.locations if loc["lat"] != 0]
        if heat_data:
            HeatMap(heat_data, radius=25, blur=15, max_zoom=6,
                gradient={0.2: 'blue', 0.5: 'lime', 0.8: 'orange', 1: 'red'}).add_to(m)
        
        # Create list of locations with valid coordinates for connection lines
        valid_locations = [loc for loc in self.locations if loc["lat"] != 0]
        
        # Draw BLINKING connection lines between locations
        if len(valid_locations) >= 2:
            for i in range(len(valid_locations) - 1):
                loc1 = valid_locations[i]
                loc2 = valid_locations[i + 1]
                
                # Determine line color based on risk
                avg_risk = (loc1["risk_score"] + loc2["risk_score"]) / 2
                if avg_risk >= 7:
                    line_class = "line-critical"
                elif avg_risk >= 4:
                    line_class = "line-high"
                elif avg_risk >= 2:
                    line_class = "line-medium"
                else:
                    line_class = "line-low"
                
                # Draw blinking polyline
                folium.PolyLine(
                    locations=[[loc1["lat"], loc1["lon"]], [loc2["lat"], loc2["lon"]]],
                    color="#ff0000" if avg_risk >= 7 else "#ff6600" if avg_risk >= 4 else "#ffcc00" if avg_risk >= 2 else "#00ff00",
                    weight=3,
                    opacity=0.8,
                    dash_array='5, 5',
                    className=line_class,
                    popup=f"Connection: {loc1['ip']} → {loc2['ip']}<br>Risk: {avg_risk:.1f}"
                ).add_to(m)
                
                # Add animated directional arrow (small circle along the line)
                mid_lat = (loc1["lat"] + loc2["lat"]) / 2
                mid_lon = (loc1["lon"] + loc2["lon"]) / 2
                
                folium.CircleMarker(
                    location=[mid_lat, mid_lon],
                    radius=4,
                    color="#00ffff",
                    fill=True,
                    fill_color="#00ffff",
                    fill_opacity=0.8,
                    className="animated-line",
                    popup="Data Flow Direction"
                ).add_to(m)
        
        # Add BLINKING markers
        for loc in self.locations:
            if loc["lat"] == 0:
                continue
            
            risk = loc["risk_score"]
            if risk >= 7:
                color = "#ff0000"
                blink_class = "blink-critical"
                radius = 16
                icon = "💀"
                pulse_radius = 200000  # Large pulse for critical
            elif risk >= 4:
                color = "#ff6600"
                blink_class = "blink-high"
                radius = 13
                icon = "⚠️"
                pulse_radius = 150000
            elif risk >= 2:
                color = "#ffcc00"
                blink_class = "blink-medium"
                radius = 10
                icon = "●"
                pulse_radius = 100000
            else:
                color = "#00ff00"
                blink_class = "blink-low"
                radius = 7
                icon = "✓"
                pulse_radius = 50000
            
            # Build popup HTML
            if loc.get("is_organization_location", False):
                popup_html = f"""
                <div style="font-family: monospace; background: #0a0a0a; color: #00ff00; padding: 12px; border-radius: 8px; min-width: 320px;">
                    <b style="color: #00ffff;">🏢 {loc.get('domain', loc['ip'])}</b><br>
                    <hr style="border-color: #333; margin: 5px 0;">
                    
                    <b>📍 ORGANIZATION HEADQUARTERS:</b><br>
                    <span style="color: #ffcc00;">  {loc.get('flag', '🌐')} {loc['country']} - {loc.get('city', 'Unknown')}</span><br>
                    
                    <b>🖥️ SERVER/CLOUD LOCATION:</b><br>
                    <span style="color: #ff6600;">  🌍 {loc.get('server_location', 'Unknown')}</span><br>
                    
                    <b>⚠️ Risk Score:</b> <span style="color: {color}; font-weight: bold;">{risk}/10</span><br>
                    <b>🔓 Open Ports:</b> {len(loc.get('ports', []))}<br>
                    <b>🔧 Services:</b> {', '.join([p.get('service', 'unknown') for p in loc.get('ports', [])[:3]])}<br>
                    
                    <hr style="border-color: #333; margin: 5px 0;">
                    <span style="color: #888; font-size: 10px;">ℹ️ Organization uses CDN/Cloud hosting - showing HQ location</span>
                    <br><span style="color: #ff6600; font-size: 10px;">🔘 Blinking circle indicates live monitoring</span>
                </div>
                """
                # Add star marker for organization headquarters
                folium.Marker(
                    location=[loc["lat"], loc["lon"]],
                    icon=folium.Icon(color="orange", icon="star", prefix="fa"),
                    popup=folium.Popup(popup_html, max_width=400)
                ).add_to(m)
            else:
                popup_html = f"""
                <div style="font-family: monospace; background: #0a0a0a; color: #00ff00; padding: 12px; border-radius: 8px; min-width: 280px;">
                    <b style="color: #00ffff;">🎯 {loc.get('domain', loc['ip'])}</b><br>
                    <hr style="border-color: #333; margin: 5px 0;">
                    
                    <b>🖥️ SERVER LOCATION:</b><br>
                    <span style="color: #ffcc00;">  {loc.get('flag', '🌐')} {loc['country']} - {loc.get('city', 'Unknown')}</span><br>
                    
                    <b>⚠️ Risk Score:</b> <span style="color: {color}; font-weight: bold;">{risk}/10</span><br>
                    <b>🔓 Open Ports:</b> {len(loc.get('ports', []))}<br>
                    <b>🔧 Services:</b> {', '.join([p.get('service', 'unknown') for p in loc.get('ports', [])[:3]])}<br>
                    
                    <hr style="border-color: #333; margin: 5px 0;">
                    <span style="color: #888; font-size: 10px;">ℹ️ Server location detected via GeoIP</span>
                    <br><span style="color: #ff6600; font-size: 10px;">🔘 Blinking circle indicates live monitoring</span>
                </div>
                """
                
                # Add BLINKING circle marker
                folium.CircleMarker(
                    location=[loc["lat"], loc["lon"]],
                    radius=radius,
                    popup=folium.Popup(popup_html, max_width=350),
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.8,
                    weight=3,
                    className=blink_class
                ).add_to(m)
            
            # Add PULSE RING effect for critical/high risk
            if risk >= 4:
                folium.Circle(
                    location=[loc["lat"], loc["lon"]],
                    radius=pulse_radius,
                    color=color,
                    fill=True,
                    fill_opacity=0.05,
                    weight=2,
                    className="pulse-ring",
                    popup=f"⚠️ Active Threat Zone - Risk Level: {risk}/10"
                ).add_to(m)
        
        # Add BLINKING connection lines between all location pairs (network mesh)
        if len(valid_locations) >= 2:
            for i in range(len(valid_locations)):
                for j in range(i + 1, len(valid_locations)):
                    loc1 = valid_locations[i]
                    loc2 = valid_locations[j]
                    
                    # Calculate distance-based risk
                    dist_risk = (loc1["risk_score"] + loc2["risk_score"]) / 2
                    
                    if dist_risk >= 7:
                        line_color = "#ff0000"
                        line_class = "line-critical"
                        weight = 3
                    elif dist_risk >= 4:
                        line_color = "#ff6600"
                        line_class = "line-high"
                        weight = 2.5
                    elif dist_risk >= 2:
                        line_color = "#ffcc00"
                        line_class = "line-medium"
                        weight = 2
                    else:
                        line_color = "#00ff00"
                        line_class = "line-low"
                        weight = 1.5
                    
                    folium.PolyLine(
                        locations=[[loc1["lat"], loc1["lon"]], [loc2["lat"], loc2["lon"]]],
                        color=line_color,
                        weight=weight,
                        opacity=0.7,
                        dash_array='8, 6',
                        className=line_class,
                        popup=f"Network Link<br>{loc1['ip']} ↔ {loc2['ip']}<br>Risk: {dist_risk:.1f}"
                    ).add_to(m)
        
        # Legend with blinking indicators
        legend_html = '''
        <div style="position: fixed; bottom: 20px; right: 20px; z-index: 1000; background: rgba(0,0,0,0.85); padding: 12px; border-radius: 8px; border: 1px solid #00ff00; font-family: monospace; font-size: 10px;">
            <b style="color: #00ff00;">🗺️ THREAT LEGEND</b><br>
            <span style="color:#ff0000; animation: blink-red 0.6s infinite;">🔴</span> Critical (Risk 7-10)<br>
            <span style="color:#ff6600; animation: blink-orange 0.8s infinite;">🟠</span> High (Risk 5-6)<br>
            <span style="color:#ffcc00; animation: blink-yellow 1s infinite;">🟡</span> Medium (Risk 3-4)<br>
            <span style="color:#00ff00; animation: blink-green 1.2s infinite;">🟢</span> Low (Risk 0-2)<br>
            <span style="color:#ffaa00;">⭐</span> Organization Headquarters<br>
            <span style="color:#00ffff;">━━━</span> <span style="animation: blink-green 1s infinite;">Blinking Connection</span><br>
            <span style="color:#ff00ff;">◉</span> <span style="animation: blink-red 1s infinite;">Pulse Ring = Active Threat Zone</span>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))
        
        return m._repr_html_()
class InteractiveSOCDashboard:
    def __init__(self):
        self.workspace = os.path.expanduser("~/dsterminal_workspace")
        self.scans_dir = os.path.join(self.workspace, "scans")
        os.makedirs(self.scans_dir, exist_ok=True)
        
        self.network_nodes: Dict[str, NetworkNode] = {}
        self.discovered_ports = []
        self.services_found = []
        self.scan_duration = 0
        self.current_target = ""
        self.scan_active = False
        self.ai_scorer = AIVulnerabilityScorer()
        self.geo_map = EnhancedGeoMapVisualizer()
        self.scan_history: List[ScanHistory] = []
        

        # Load history from file
        self.history_file = os.path.join(self.scans_dir, "scan_history.json")
        self._load_history()
        
        # Terminal display settings
        self.spinner_frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.terminal_width = self._get_terminal_width()

    def _get_terminal_width(self):
        """Get terminal width safely"""
        try:
            return shutil.get_terminal_size((100, 24)).columns
        except:
            return 100
    def _load_history(self):
        """Load scan history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    data = json.load(f)
                    for item in data:
                        hist = ScanHistory(
                            timestamp=datetime.fromisoformat(item['timestamp']),
                            target=item['target'],
                            duration=item['duration'],
                            open_ports=item['open_ports'],
                            risk_score=item['risk_score'],
                            services=item['services']
                        )
                        self.scan_history.append(hist)
            except:
                pass
    
    def _save_history(self):
        """Save scan history to file"""
        try:
            data = []
            for hist in self.scan_history:
                data.append({
                    'timestamp': hist.timestamp.isoformat(),
                    'target': hist.target,
                    'duration': hist.duration,
                    'open_ports': hist.open_ports,
                    'risk_score': hist.risk_score,
                    'services': hist.services
                })
            with open(self.history_file, 'w') as f:
                json.dump(data, f, indent=2)
        except:
            pass
        
    def generate_pdf_report(self, target: str = None) -> str:
        """Generate professional PDF report of scan results"""
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib.enums import TA_CENTER, TA_LEFT
            from reportlab.pdfgen import canvas
            import datetime
            
            # Create PDF filename
            if not target:
                target = self.current_target if self.current_target else "scan"
            
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            pdf_filename = f"soc_report_{target.replace('.', '_')}_{timestamp}.pdf"
            pdf_path = os.path.join(self.scans_dir, pdf_filename)
            
            # Create the PDF document
            doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                                    rightMargin=72, leftMargin=72,
                                    topMargin=72, bottomMargin=72)
            
            # Styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#00ff00'),
                alignment=TA_CENTER,
                spaceAfter=30
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#00ffff'),
                spaceAfter=12,
                spaceBefore=12
            )
            
            risk_high_style = ParagraphStyle(
                'RiskHigh',
                parent=styles['Normal'],
                textColor=colors.HexColor('#ff0000'),
                fontSize=10
            )
            
            risk_medium_style = ParagraphStyle(
                'RiskMedium',
                parent=styles['Normal'],
                textColor=colors.HexColor('#ffcc00'),
                fontSize=10
            )
            
            risk_low_style = ParagraphStyle(
                'RiskLow',
                parent=styles['Normal'],
                textColor=colors.HexColor('#00ff00'),
                fontSize=10
            )
            
            # Build story (content)
            story = []
            
            # Title
            story.append(Paragraph("DSTERMINAL SOC Security Assessment Report", title_style))
            story.append(Spacer(1, 12))
            
            # Report metadata
            story.append(Paragraph(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            story.append(Paragraph(f"Target: {target}", styles['Normal']))
            story.append(Paragraph(f"Scan Duration: {self.scan_duration} seconds", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Executive Summary
            story.append(Paragraph("Executive Summary", heading_style))
            
            total_risk = sum(p.get("risk_score", 0) for p in self.discovered_ports)
            avg_risk = total_risk / max(1, len(self.discovered_ports))
            
            if avg_risk >= 7:
                risk_level = "CRITICAL"
                risk_color = colors.HexColor('#ff0000')
            elif avg_risk >= 4:
                risk_level = "WARNING"
                risk_color = colors.HexColor('#ffcc00')
            else:
                risk_level = "LOW"
                risk_color = colors.HexColor('#00ff00')
            
            summary_text = f"""
            <b>Risk Assessment Score: {avg_risk:.1f}/10 - {risk_level}</b><br/>
            <br/>
            This report summarizes the security assessment performed on {target}. 
            The scan identified {len(self.network_nodes)} host(s) with {len(self.discovered_ports)} open ports 
            and {len(self.services_found)} active services.<br/>
            <br/>
            <b>Key Findings:</b><br/>
            • Total Open Ports: {len(self.discovered_ports)}<br/>
            • Total Services: {len(self.services_found)}<br/>
            • Average Risk Score: {avg_risk:.1f}/10<br/>
            • Scan Duration: {self.scan_duration} seconds
            """
            story.append(Paragraph(summary_text, styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Discovered Services Table
            story.append(Paragraph("Discovered Services & Vulnerabilities", heading_style))
            
            if self.services_found:
                # Table data
                table_data = [['Port', 'Service', 'Version', 'Risk Score', 'Exploit', 'CVE ID']]
                
                for service in self.services_found[:20]:  # Limit to 20 for PDF
                    risk_score = service.get("risk_score", 0)
                    risk_str = f"{risk_score:.1f}"
                    
                    table_data.append([
                        f"{service['port']}/{service['protocol']}",
                        service['service'][:20],
                        service.get('version', 'N/A')[:15],
                        risk_str,
                        service.get('exploit', 'N/A')[:15],
                        service.get('cvss_id', 'N/A')
                    ])
                
                # Create table
                table = Table(table_data, colWidths=[60, 80, 70, 50, 80, 70])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00ffff')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                ]))
                story.append(table)
            else:
                story.append(Paragraph("No services discovered during the scan.", styles['Normal']))
            
            story.append(Spacer(1, 20))
            
            # Critical Findings (High Risk)
            high_risk = [s for s in self.services_found if s.get("risk_score", 0) >= 7]
            if high_risk:
                story.append(Paragraph("Critical Findings (High Risk)", heading_style))
                for service in high_risk[:10]:
                    finding_text = f"""
                    <b>• {service['port']}/{service['protocol']} - {service['service']}</b><br/>
                    Risk Score: {service['risk_score']}/10 | CVE: {service.get('cvss_id', 'N/A')}<br/>
                    Exploit: {service.get('exploit', 'N/A')}<br/>
                    Recommendation: {service.get('recommendation', 'Patch immediately')}
                    """
                    story.append(Paragraph(finding_text, risk_high_style))
                    story.append(Spacer(1, 10))
            
            # Medium Risk Findings
            medium_risk = [s for s in self.services_found if 4 <= s.get("risk_score", 0) < 7]
            if medium_risk:
                story.append(Paragraph("Medium Risk Findings", heading_style))
                for service in medium_risk[:10]:
                    finding_text = f"""
                    <b>• {service['port']}/{service['protocol']} - {service['service']}</b><br/>
                    Risk Score: {service['risk_score']}/10 | CVE: {service.get('cvss_id', 'N/A')}
                    """
                    story.append(Paragraph(finding_text, risk_medium_style))
                    story.append(Spacer(1, 10))
            
            story.append(PageBreak())
            
            # Network Topology
            story.append(Paragraph("Network Topology Analysis", heading_style))
            
            if self.network_nodes:
                topo_data = [['Host', 'Open Ports', 'Risk Score', 'Location Type']]
                for ip, node in self.network_nodes.items():
                    location_type = "🏢 HQ" if node.is_organization_location else "🖥️ Server"
                    topo_data.append([
                        ip[:15],
                        str(len(node.ports)),
                        f"{node.risk_score:.1f}",
                        location_type
                    ])
                
                topo_table = Table(topo_data, colWidths=[100, 70, 70, 80])
                topo_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00ffff')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                ]))
                story.append(topo_table)
            else:
                story.append(Paragraph("No network topology data available.", styles['Normal']))
            
            story.append(Spacer(1, 20))
            
            # Recommendations
            story.append(Paragraph("Security Recommendations", heading_style))
            
            recommendations = []
            for service in self.services_found:
                if service.get("risk_score", 0) >= 7:
                    recommendations.append(f"• CRITICAL: Patch {service['service']} on port {service['port']} immediately")
                elif service.get("risk_score", 0) >= 4:
                    recommendations.append(f"• MEDIUM: Update {service['service']} on port {service['port']}")
            
            if recommendations:
                for rec in recommendations[:10]:
                    story.append(Paragraph(rec, styles['Normal']))
                    story.append(Spacer(1, 5))
            else:
                story.append(Paragraph("No critical recommendations at this time. Continue regular security monitoring.", styles['Normal']))
            
            story.append(Spacer(1, 20))
            
            # Footer note
            story.append(Paragraph("This report was automatically generated by DSTERMINAL Cyber-Ops Platform", styles['Normal']))
            story.append(Paragraph("For questions or support, contact your security team.", styles['Normal']))
            
            # Build PDF
            doc.build(story)
            
            print(f"{Colors.GREEN}[+] PDF Report generated: {pdf_path}{Colors.RESET}")
            return pdf_path
            
        except ImportError:
            print(f"{Colors.RED}[!] ReportLab not installed. Install with: pip install reportlab{Colors.RESET}")
            return None
        except Exception as e:
            print(f"{Colors.RED}[!] PDF generation failed: {e}{Colors.RESET}")
            return None
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def center(self, text: str) -> str:
        return text.center(self.terminal_width)
    
    def draw_header(self):
        header = f"""
{Colors.RED}{Colors.BOLD}
{self.center("╔" + "═" * 76 + "╗")}
{self.center("║" + " " * 76 + "║")}
{self.center("║" + " " * 10 + "██████╗ ███████╗████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗" + " " * 10 + "║")}
{self.center("║" + " " * 10 + "██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║" + " " * 10 + "║")}
{self.center("║" + " " * 10 + "██║  ██║███████╗   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║" + " " * 10 + "║")}
{self.center("║" + " " * 10 + "██║  ██║╚════██║   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║" + " " * 10 + "║")}
{self.center("║" + " " * 10 + "██████╔╝███████╗   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗" + " " * 10 + "║")}
{self.center("║" + " " * 10 + "╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝" + " " * 10 + "║")}
{self.center("║" + " " * 76 + "║")}
{self.center("║" + " " * 20 + Colors.YELLOW + "⚡ SOC-GRADE NETWORK INTELLIGENCE ⚡" + Colors.RED + " " * 20 + "║")}
{self.center("║" + " " * 25 + Colors.DIM + "Real-time Scanning | AI Scoring | Threat Intelligence | DNS Reconnaissance" + Colors.RED + " " * 25 + "║")}
{self.center("║" + " " * 76 + "║")}
{self.center("╚" + "═" * 76 + "╝")}
{Colors.RESET}
"""
        print(header)
    
    def draw_centered_dashboard(self):
        """
        Ultra-centered SOC dashboard with:
        LEFT PANEL  | CENTER PANEL | RIGHT PANEL
        """
        # Get actual terminal width safely
        try:
            terminal_width = shutil.get_terminal_size((80, 24)).columns
        except:
            terminal_width = 80
        
        # Adjust panel widths based on terminal size
        if terminal_width < 120:
            panel_width = 38
            spacing = 5

        elif terminal_width < 150:
            panel_width = 38
            spacing = 5
        else:
            panel_width = 35
            spacing = 45
        
        total_width = (panel_width * 3) + (spacing * 2)
        left_padding = max(0, (terminal_width - total_width) // 2)
        pad = " " * left_padding

        # =========================================================
        # LEFT PANEL
        # =========================================================

        left_panel = [
            f"{Colors.CYAN}┌{'─' * panel_width}┐{Colors.RESET}",
            f"{Colors.CYAN}│{Colors.RESET} {Colors.BOLD}{Colors.GREEN}🎯 SCAN CONTROL CENTER{Colors.RESET}{' ' * 8}{Colors.CYAN}│{Colors.RESET}",
            f"{Colors.CYAN}├{'─' * panel_width}┤{Colors.RESET}",

            f"{Colors.CYAN}│{Colors.RESET} {Colors.YELLOW}[1]{Colors.RESET} Quick Scan{' ' * 18}{Colors.CYAN}│{Colors.RESET}",
            f"{Colors.CYAN}│{Colors.RESET} {Colors.YELLOW}[2]{Colors.RESET} Standard Scan{' ' * 15}{Colors.CYAN}│{Colors.RESET}",
            f"{Colors.CYAN}│{Colors.RESET} {Colors.YELLOW}[3]{Colors.RESET} Full Aggressive{' ' * 13}{Colors.CYAN}│{Colors.RESET}",
            f"{Colors.CYAN}│{Colors.RESET} {Colors.YELLOW}[4]{Colors.RESET} DNS Recon{' ' * 20}{Colors.CYAN}│{Colors.RESET}",
            f"{Colors.CYAN}│{Colors.RESET} {Colors.YELLOW}[5]{Colors.RESET} UDP Scan{' ' * 20}{Colors.CYAN}│{Colors.RESET}",

            f"{Colors.CYAN}├{'─' * panel_width}┤{Colors.RESET}",

            f"{Colors.CYAN}│{Colors.RESET} Target : {Colors.GREEN}{self.current_target[:18]:<18}{Colors.RESET} {Colors.CYAN}│{Colors.RESET}",
            f"{Colors.CYAN}│{Colors.RESET} Status : {Colors.RED if self.scan_active else Colors.YELLOW}{'● ACTIVE' if self.scan_active else '○ IDLE'}{Colors.RESET}{' ' * 17}{Colors.CYAN}│{Colors.RESET}",

            f"{Colors.CYAN}└{'─' * panel_width}┘{Colors.RESET}",
        ]

        # =========================================================
        # CENTER PANEL
        # =========================================================

        total_risk = sum(p.get("risk_score", 0) for p in self.discovered_ports)
        avg_risk = total_risk / max(1, len(self.discovered_ports))

        risk_bar_size = 22
        filled = int((avg_risk / 10) * risk_bar_size)
        risk_bar = "█" * filled + "░" * (risk_bar_size - filled)

        if avg_risk >= 7:
            risk_color = Colors.RED
            threat = "CRITICAL"
        elif avg_risk >= 4:
            risk_color = Colors.YELLOW
            threat = "WARNING"
        else:
            risk_color = Colors.GREEN
            threat = "LOW"

        center_panel = [
            f"{Colors.MAGENTA}┌{'─' * panel_width}┐{Colors.RESET}",
            f"{Colors.MAGENTA}│{Colors.RESET} {Colors.BOLD}{Colors.CYAN}🛡 SOC LIVE STATUS{Colors.RESET}{' ' * 13}{Colors.MAGENTA}│{Colors.RESET}",
            f"{Colors.MAGENTA}├{'─' * panel_width}┤{Colors.RESET}",

            f"{Colors.MAGENTA}│{Colors.RESET} Hosts Found : {Colors.GREEN}{len(self.network_nodes):<10}{Colors.RESET}{' ' * 9}{Colors.MAGENTA}│{Colors.RESET}",
            f"{Colors.MAGENTA}│{Colors.RESET} Open Ports : {Colors.GREEN}{len(self.discovered_ports):<10}{Colors.RESET}{' ' * 9}{Colors.MAGENTA}│{Colors.RESET}",
            f"{Colors.MAGENTA}│{Colors.RESET} Services    : {Colors.GREEN}{len(self.services_found):<10}{Colors.RESET}{' ' * 9}{Colors.MAGENTA}│{Colors.RESET}",
            f"{Colors.MAGENTA}│{Colors.RESET} Duration    : {Colors.GREEN}{self.scan_duration}s{' ' * 16}{Colors.RESET}{Colors.MAGENTA}│{Colors.RESET}",

            f"{Colors.MAGENTA}├{'─' * panel_width}┤{Colors.RESET}",

            f"{Colors.MAGENTA}│{Colors.RESET} Threat Level:{' ' * 18}{Colors.MAGENTA}│{Colors.RESET}",
            f"{Colors.MAGENTA}│{Colors.RESET} {risk_color}{risk_bar}{Colors.RESET} {avg_risk:.1f}/10 {Colors.MAGENTA}│{Colors.RESET}",
            f"{Colors.MAGENTA}│{Colors.RESET} Status : {risk_color}{threat}{Colors.RESET}{' ' * (21 - len(threat))}{Colors.MAGENTA}│{Colors.RESET}",

            f"{Colors.MAGENTA}└{'─' * panel_width}┘{Colors.RESET}",
        ]

        # =========================================================
        # RIGHT PANEL
        # =========================================================

        right_panel = [
            f"{Colors.BLUE}┌{'─' * panel_width}┐{Colors.RESET}",
            f"{Colors.BLUE}│{Colors.RESET} {Colors.BOLD}{Colors.YELLOW}🔍 LIVE DISCOVERIES{Colors.RESET}{' ' * 11}{Colors.BLUE}│{Colors.RESET}",
            f"{Colors.BLUE}├{'─' * panel_width}┤{Colors.RESET}",
        ]

        recent = self.discovered_ports[-6:]

        if recent:
            for p in recent:
                port = f"{p['port']}/{p['protocol']}"
                service = p["service"][:14]

                score = p.get("risk_score", 0)

                if score >= 7:
                    color = Colors.RED
                    icon = "⚠"
                elif score >= 4:
                    color = Colors.YELLOW
                    icon = "●"
                else:
                    color = Colors.GREEN
                    icon = "✓"

                line = f"{icon} {port:<10} {service:<14}"

                right_panel.append(
                    f"{Colors.BLUE}│{Colors.RESET} {color}{line:<32}{Colors.RESET}{Colors.BLUE}│{Colors.RESET}"
                )
        else:
            for _ in range(6):
                right_panel.append(
                    f"{Colors.BLUE}│{Colors.RESET} {Colors.DIM}Waiting for scan results...{Colors.RESET}{' ' * 4}{Colors.BLUE}│{Colors.RESET}"
                )

        right_panel.extend([
            f"{Colors.BLUE}├{'─' * panel_width}┤{Colors.RESET}",
            f"{Colors.BLUE}│{Colors.RESET} Updated : {Colors.GREEN}{datetime.now().strftime('%H:%M:%S')}{Colors.RESET}{' ' * 12}{Colors.BLUE}│{Colors.RESET}",
            f"{Colors.BLUE}└{'─' * panel_width}┘{Colors.RESET}",
        ])

        # =========================================================
        # RENDER DASHBOARD
        # =========================================================

        max_lines = max(
            len(left_panel),
            len(center_panel),
            len(right_panel)
        )

        for i in range(max_lines):

            left = left_panel[i] if i < len(left_panel) else " " * (panel_width + 2)
            center = center_panel[i] if i < len(center_panel) else " " * (panel_width + 2)
            right = right_panel[i] if i < len(right_panel) else " " * (panel_width + 2)

            print(
                pad +
                left +
                (" " * spacing) +
                center +
                (" " * spacing) +
                right
            )
    
    def draw_results_table(self):
        if not self.services_found:
            print(f"\n{self.center(Colors.YELLOW + '─' * 70 + Colors.RESET)}")
            print(self.center(Colors.YELLOW + ' ' * 28 + '⚠ NO RESULTS YET ⚠' + Colors.RESET))
            print(self.center(Colors.YELLOW + '─' * 70 + Colors.RESET))
            return
        
        print(f"\n{self.center(Colors.CYAN + Colors.BOLD + '─' * 90 + Colors.RESET)}")
        print(self.center(Colors.CYAN + Colors.BOLD + '│' + ' ' * 38 + '🔓 DISCOVERED SERVICES 🔓' + ' ' * 38 + '│' + Colors.RESET))
        print(self.center(Colors.CYAN + Colors.BOLD + '─' * 90 + Colors.RESET))
        
        header = f"{Colors.CYAN}│ {Colors.GREEN}PORT{Colors.RESET} │ {Colors.GREEN}SERVICE{Colors.RESET} │ {Colors.GREEN}VERSION{Colors.RESET} │ {Colors.GREEN}RISK{Colors.RESET} │ {Colors.GREEN}EXPLOIT{Colors.RESET} │{Colors.CYAN}"
        print(self.center(header))
        print(self.center(Colors.CYAN + '─' * 90 + Colors.RESET))
        
        for service in self.services_found[:8]:
            risk_score = service.get("risk_score", 0)
            if risk_score >= 7:
                risk_text = f"{Colors.RED}⚠ HIGH ⚠{Colors.RESET}"
            elif risk_score >= 4:
                risk_text = f"{Colors.YELLOW}● MED ●{Colors.RESET}"
            else:
                risk_text = f"{Colors.GREEN}○ LOW ○{Colors.RESET}"
            
            exploit_info = service.get("exploit", "N/A")[:10]
            line = f"{Colors.CYAN}│{Colors.RESET} {Colors.GREEN}{service['port']}/{service['protocol']:<4}{Colors.RESET} │ {Colors.CYAN}{service['service'][:10]:<10}{Colors.RESET} │ {Colors.DIM}{service.get('version', 'N/A')[:8]:<8}{Colors.RESET} │ {risk_text:<10} │ {Colors.PURPLE}{exploit_info:<10}{Colors.RESET} │{Colors.CYAN}"
            print(self.center(line))
        
        print(self.center(Colors.CYAN + '─' * 90 + Colors.RESET))
    
    def draw_footer(self):
        footer = f"""
{Colors.DIM}{self.center('═' * 90)}{Colors.RESET}
{self.center(Colors.DIM + ' Commands: ' + Colors.GREEN + '[S]' + Colors.DIM + ' Scan  ' + Colors.YELLOW + '[Q]' + Colors.DIM + ' Quick  ' + Colors.RED + '[F]' + Colors.DIM + ' Full  ' + Colors.CYAN + '[D]' + Colors.DIM + ' DNS Recon  ' + Colors.MAGENTA + '[H]' + Colors.DIM + ' Help  ' + Colors.WHITE + '[X]' + Colors.DIM + ' Exit')}{Colors.RESET}
{Colors.DIM}{self.center('═' * 90)}{Colors.RESET}
"""
        print(footer)
    
    def enhanced_geoip_lookup(self, hostname: str, ip: str) -> Tuple[Dict, bool]:
        """Enhanced GeoIP lookup with organization location override"""
        # First, check if we have the organization's headquarters location
        org_location = OrganizationLocationDB.get_organization_location(hostname, ip)
        
        if org_location and org_location.get("lat", 0) != 0:
            # Get server location for comparison
            try:
                response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
                server_data = response.json()
                server_location = f"{server_data.get('city', 'Unknown')}, {server_data.get('country', 'Unknown')}"
            except:
                server_location = "Unknown"
            
            return {
                "country": org_location["country"],
                "city": org_location["city"],
                "lat": org_location["lat"],
                "lon": org_location["lon"],
                "flag": org_location.get("flag", "🌐"),
                "is_organization_location": True,
                "server_location": server_location,
                "note": f"Showing organization headquarters in {org_location['country']}"
            }, True
        
        # Fallback to server location
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
            data = response.json()
            return {
                "country": data.get("country", "Unknown"),
                "city": data.get("city", "Unknown"),
                "lat": data.get("lat", 0),
                "lon": data.get("lon", 0),
                "flag": "🌐",
                "is_organization_location": False
            }, False
        except:
            return {"country": "Unknown", "city": "Unknown", "lat": 0, "lon": 0, "flag": "🌐", "is_organization_location": False}, False
    
    def parse_nmap_output(self, line: str):
        line = line.strip()
        if not line:
            return
        
        host_match = re.search(r'Nmap scan report for (.+)', line)
        if host_match:
            host = host_match.group(1).strip()
            host = re.sub(r'\([^)]*\)', '', host).strip()
            if host not in self.network_nodes:
                # Use enhanced GeoIP lookup
                geo, is_org_location = self.enhanced_geoip_lookup(host, host)
                node = NetworkNode(
                    ip=host, 
                    country=geo.get("country", "Unknown"), 
                    lat=geo.get("lat", 0), 
                    lon=geo.get("lon", 0),
                    is_organization_location=is_org_location,
                    server_location=geo.get("server_location", "")
                )
                self.network_nodes[host] = node
                if geo.get("lat", 0) != 0:
                    self.geo_map.add_location(
                        geo["lat"], geo["lon"], host, 0, [], 
                        geo.get("country", "Unknown"),
                        is_org_location,
                        geo.get("server_location", ""),
                        host
                    )
            return
        
        port_match = re.search(r'(\d+)/(tcp|udp)\s+open\s+(\S+)', line)
        if port_match:
            port = port_match.group(1)
            proto = port_match.group(2)
            service = port_match.group(3).replace('?', '').strip()
            
            version = ""
            rest = line[port_match.end():].strip()
            if rest and not rest.startswith('syn-'):
                version = rest[:30]
            
            vuln = self.ai_scorer.analyze_service(service, port, version)
            risk_score = vuln["cvss_score"]
            
            self.discovered_ports.append({"port": port, "protocol": proto, "service": service, "version": version, "risk_score": risk_score})
            self.services_found.append({
                "port": port, "protocol": proto, "service": service, "version": version,
                "risk_score": risk_score, "exploit": vuln.get("exploit", "N/A"),
                "cvss_id": vuln.get("cvss_id", "N/A")
            })
            
            for node in self.network_nodes.values():
                if node.lat != 0:
                    node.ports.append({"port": port, "service": service, "risk_score": risk_score})
                    node.risk_score = max(node.risk_score, risk_score)
                    self.geo_map.add_location(
                        node.lat, node.lon, node.ip, node.risk_score, node.ports, 
                        node.country, node.is_organization_location, node.server_location, node.ip
                    )
            
            color = Colors.RED if risk_score >= 7 else Colors.YELLOW if risk_score >= 4 else Colors.GREEN
            spinner = random.choice(self.spinner_frames)
            print(f"\r{self.center(f'{Colors.CYAN}[{spinner}]{Colors.RESET} {color}[!] NEW: {port} - {service} (Risk: {risk_score}){Colors.RESET}')}")
            time.sleep(0.05)
            return
        
        if "Nmap done" in line:
            self.scan_active = False
    
    def run_nmap_scan(self, target: str, flags: List[str]):
        if not shutil.which("nmap"):
            print(self.center(f"{Colors.RED}[!] Nmap not installed{Colors.RESET}"))
            return
        
        self.current_target = target
        self.scan_active = True
        self.discovered_ports = []
        self.services_found = []
        self.network_nodes = {}
        self.geo_map = EnhancedGeoMapVisualizer()
        
        start_time = datetime.now()
        cmd = ["nmap"] + flags + [target]
        
        print(f"\n{self.center(Colors.GREEN + '[+] Running: ' + ' '.join(cmd) + Colors.RESET)}\n")
        
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
            for line in process.stdout:
                self.parse_nmap_output(line)
            process.wait()
            self.scan_duration = (datetime.now() - start_time).seconds
            self.scan_active = False
            
            # Save to history
            services_list = [s['service'] for s in self.services_found]
            history = ScanHistory(
                timestamp=datetime.now(),
                target=target,
                duration=self.scan_duration,
                open_ports=len(self.discovered_ports),
                risk_score=sum(p.get('risk_score', 0) for p in self.discovered_ports) / max(1, len(self.discovered_ports)),
                services=services_list[:5]
            )
            self.scan_history.append(history)
            self._save_history()  # Save to file
            if len(self.scan_history) > 10:
                self.scan_history.pop(0)
            
            print(f"\n{self.center(Colors.GREEN + '[+] Scan completed in ' + str(self.scan_duration) + 's' + Colors.RESET)}")
            print(self.center(Colors.CYAN + '[+] Found ' + str(len(self.discovered_ports)) + ' open ports' + Colors.RESET))
            
            print(self.center(Colors.YELLOW + '[+] Opening GeoMap dashboard with organization locations...' + Colors.RESET))
            self.generate_full_dashboard()

            # Generate PDF report as well
            print(self.center(Colors.CYAN + '[+] Generating PDF report...' + Colors.RESET))
            pdf_path = self.generate_pdf_report(target)
            if pdf_path:
                print(self.center(Colors.GREEN + f'[+] PDF saved: {pdf_path}' + Colors.RESET))
        except Exception as e:
            print(self.center(f"{Colors.RED}[!] Scan failed: {e}{Colors.RESET}"))
            self.scan_active = False
    
    def generate_network_topology(self) -> str:
        """Generate network topology visualization using Plotly"""
        if not PLOTLY_AVAILABLE or not self.network_nodes:
            return '<div style="padding:50px;text-align:center;">No topology data available</div>'
        
        node_list = list(self.network_nodes.keys())
        num_nodes = len(node_list)
        
        node_x = []
        node_y = []
        node_text = []
        node_colors = []
        node_sizes = []
        
        for i, ip in enumerate(node_list):
            angle = 2 * math.pi * i / max(1, num_nodes)
            radius = 4
            node_x.append(radius * math.cos(angle))
            node_y.append(radius * math.sin(angle))
            risk = self.network_nodes[ip].risk_score
            is_org = self.network_nodes[ip].is_organization_location
            location_note = "🏢 HQ" if is_org else "🖥️ Server"
            node_text.append(f"{ip}<br>{location_note}<br>Risk: {risk:.1f}<br>Ports: {len(self.network_nodes[ip].ports)}")
            
            if risk >= 7:
                node_colors.append("#ff0000")
                node_sizes.append(25)
            elif risk >= 4:
                node_colors.append("#ffcc00")
                node_sizes.append(20)
            else:
                node_colors.append("#00ff00")
                node_sizes.append(15)
        
        edge_x = []
        edge_y = []
        for i in range(len(node_x) - 1):
            edge_x.extend([node_x[i], node_x[i+1], None])
            edge_y.extend([node_y[i], node_y[i+1], None])
        
        fig = go.Figure()
        
        if edge_x:
            fig.add_trace(go.Scatter(
                x=edge_x, y=edge_y,
                mode='lines',
                line=dict(width=2, color='#00ffff', dash='dash'),
                hoverinfo='none',
                showlegend=False
            ))
        
        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            marker=dict(size=node_sizes, color=node_colors, line=dict(width=2, color='white')),
            text=[ip[:15] for ip in node_list],
            textposition="top center",
            textfont=dict(size=10, color='white'),
            hovertext=node_text,
            hoverinfo='text',
            showlegend=False
        ))
        
        fig.update_layout(
            title=dict(text="🌐 NETWORK TOPOLOGY", font=dict(color='#00ffff', size=14), x=0.5),
            showlegend=False,
            hovermode='closest',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-6, 6]),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-6, 6]),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=400,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        
        return fig.to_html(include_plotlyjs='cdn', full_html=False)
    
    def generate_historical_timeline(self) -> str:
        """Generate historical scan timeline using Plotly"""
        if not PLOTLY_AVAILABLE or not self.scan_history:
            return '<div style="padding:50px;text-align:center;">No historical data available. Run scans to see timeline.</div>'
        
        timestamps = [h.timestamp for h in self.scan_history]
        risk_scores = [h.risk_score for h in self.scan_history]
        open_ports = [h.open_ports for h in self.scan_history]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=timestamps, y=risk_scores,
            mode='lines+markers',
            name='Risk Score',
            line=dict(color='#ff4444', width=2),
            marker=dict(size=8, color='#ff0000', symbol='diamond')
        ))
        
        fig.add_trace(go.Scatter(
            x=timestamps, y=open_ports,
            mode='lines+markers',
            name='Open Ports',
            line=dict(color='#44ff44', width=2),
            marker=dict(size=8, color='#00ff00', symbol='circle')
        ))
        
        fig.update_layout(
            title=dict(text="📊 HISTORICAL SCAN TIMELINE", font=dict(color='#00ffff', size=14), x=0.5),
            xaxis_title="Scan Time",
            yaxis_title="Value",
            template="plotly_dark",
            height=350,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            legend=dict(x=0.02, y=0.98, bgcolor='rgba(0,0,0,0.5)'),
            hovermode='x unified'
        )
        
        return fig.to_html(include_plotlyjs='cdn', full_html=False)
    
    def generate_full_dashboard(self):
        """Generate complete dashboard with GeoMap, Topology, Timeline, and Services"""
        
        total_risk = sum(p.get('risk_score', 0) for p in self.discovered_ports)
        avg_risk = total_risk / max(1, len(self.discovered_ports))
        
        # Generate services table
        services_html = ""
        for s in self.services_found[:20]:
            risk_color = "#ff0000" if s["risk_score"] >= 7 else "#ffcc00" if s["risk_score"] >= 4 else "#00ff00"
            services_html += f"""
            <tr>
                <td style="color:#00ffff">{s['port']}/{s['protocol']}</td>
                <td style="color:#00ff88">{s['service']}</td>
                <td style="color:{risk_color}; font-weight:bold">{s['risk_score']}</td>
                <td style="color:#ffcc00">{s.get('exploit', 'N/A')}</td>
                <td style="color:#ff66ff">{s.get('cvss_id', 'N/A')}</td>
            </tr>
            """
        
        geo_html = self.geo_map.generate_threat_map()
        topology_html = self.generate_network_topology()
        timeline_html = self.generate_historical_timeline()
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>DSTerminal SOC Dashboard - Full Intelligence Report</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ background: linear-gradient(135deg, #0a0a1a 0%, #0d1117 100%); font-family: 'Segoe UI', monospace; color: #e6e6e6; }}
        .header {{ background: linear-gradient(90deg, #1a1a2e, #16213e); padding: 20px; border-bottom: 2px solid #00ffff; text-align: center; }}
        .header h1 {{ font-size: 28px; background: linear-gradient(90deg, #00ffff, #ff00ff); -webkit-background-clip: text; background-clip: text; color: transparent; }}
        .dashboard-container {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; padding: 20px; max-width: 1600px; margin: 0 auto; }}
        .card {{ background: rgba(20, 25, 40, 0.95); border-radius: 15px; padding: 20px; border: 1px solid rgba(0, 255, 255, 0.2); }}
        .card-header {{ font-size: 16px; font-weight: bold; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid rgba(0, 255, 255, 0.3); color: #00ffff; text-align: center; }}
        .stats-grid {{ display: flex; justify-content: center; gap: 20px; margin: 20px auto; flex-wrap: wrap; max-width: 1200px; }}
        .stat {{ text-align: center; padding: 15px 25px; background: rgba(0, 0, 0, 0.3); border-radius: 10px; min-width: 100px; }}
        .stat-value {{ font-size: 32px; font-weight: bold; color: #00ff88; }}
        .stat-label {{ font-size: 11px; color: #888; margin-top: 5px; }}
        .risk-high {{ color: #ff0000; }}
        .risk-med {{ color: #ffcc00; }}
        .risk-low {{ color: #00ff00; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); font-size: 12px; }}
        th {{ color: #00ffff; }}
        .footer {{ text-align: center; padding: 20px; border-top: 1px solid rgba(255,255,255,0.1); font-size: 10px; color: #666; }}
        .blink {{ animation: blink 1s step-end infinite; }}
        @keyframes blink {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0.5; }} }}
        .full-width {{ grid-column: span 2; }}
        @media (max-width: 1000px) {{ .dashboard-container {{ grid-template-columns: 1fr; }} .full-width {{ grid-column: span 1; }} }}
        .org-badge {{ background: #ffaa00; color: #000; padding: 2px 6px; border-radius: 10px; font-size: 9px; margin-left: 5px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🛡️ DSTERMINAL CYBER-OPS NETWORK TOPOLOGY MAPPING 🛡️</h1>
        <div>Network Intelligence | AI Vulnerability Scoring | Real-time Threat Detection</div>
        <div class="blink" style="color: #00ff00; font-size: 11px; margin-top: 5px;">● FULL INTELLIGENCE DASHBOARD - ORGANIZATION LOCATION ●</div>
    </div>
    
    <div class="stats-grid">
        <div class="stat"><div class="stat-value">{len(self.network_nodes)}</div><div class="stat-label">HOSTS</div></div>
        <div class="stat"><div class="stat-value">{len(self.discovered_ports)}</div><div class="stat-label">OPEN PORTS</div></div>
        <div class="stat"><div class="stat-value">{len(self.services_found)}</div><div class="stat-label">SERVICES</div></div>
        <div class="stat"><div class="stat-value">{self.scan_duration}s</div><div class="stat-label">DURATION</div></div>
        <div class="stat"><div class="stat-value {('risk-high' if avg_risk >= 7 else 'risk-med' if avg_risk >= 4 else 'risk-low')}">{avg_risk:.1f}</div><div class="stat-label">RISK SCORE</div></div>
        <div class="stat"><div class="stat-value">{self.current_target[:15]}</div><div class="stat-label">TARGET</div></div>
    </div>
    
    <div class="dashboard-container">
        <div class="card">
            <div class="card-header">🌍 GEOGRAPHIC THREAT MAP <span class="org-badge">🏢 HQ Locations Shown</span></div>
            <div id="geomap" style="height: 450px;">{geo_html}</div>
        </div>
        <div class="card">
            <div class="card-header">🌐 NETWORK TOPOLOGY</div>
            <div id="topology">{topology_html}</div>
        </div>
        <div class="card full-width">
            <div class="card-header">📊 HISTORICAL SCAN TIMELINE</div>
            <div id="timeline">{timeline_html}</div>
        </div>
        <div class="card full-width">
            <div class="card-header">🎯 DISCOVERED SERVICES & VULNERABILITIES</div>
            <div style="max-height: 300px; overflow: auto;">
                <table>
                    <thead>
                        <tr><th>Port</th><th>Service</th><th>Risk</th><th>Exploit</th><th>CVE ID</th></tr>
                    </thead>
                    <tbody>
                        {services_html if services_html else '<tr><td colspan="5" style="text-align:center;">No services discovered</td></tr>'}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    
    <div class="footer">
        DSTerminal Enterprise SOC Platform | Powered by AI Vulnerability Scoring | Threat Intelligence Active
        <br>📄 DSTerminal autogenerated report | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        <br><span style="color: #00ff00;">● GEOLOCATION: IP-API.COM | 🏢 ORGANIZATION HEADQUARTERS LOCATIONS | ● REAL-TIME MONITORING ACTIVE ●</span>
    </div>
</body>
</html>
        """
        
        html_path = os.path.join(self.scans_dir, f"soc_full_dashboard_{self.current_target.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        webbrowser.open(f"file://{html_path}")
        # print(self.center(f"{Colors.GREEN}[+] Full dashboard opened: {html_path}{Colors.RESET}"))
        return html_path
    
    def interactive_loop(self):
        self.clear_screen()
        
        while True:
            self.clear_screen()
            self.draw_header()
            self.draw_centered_dashboard()
            self.draw_results_table()
            self.draw_footer()
            
            choice = input(f"\n{self.center(Colors.GREEN + '[SOC] > ' + Colors.RESET)}").strip().lower()
            
            if choice == 'x':
                print(self.center(Colors.GREEN + '[+] Exiting SOC Dashboard...' + Colors.RESET))
                break
            elif choice == 's':
                target = input(self.center(Colors.CYAN + 'Enter target IP/Domain: ' + Colors.RESET))
                if target:
                    self.run_nmap_scan(target, ["-F", "-T4", "-sV"])
            elif choice == 'q':
                target = input(self.center(Colors.CYAN + 'Enter target IP/Domain: ' + Colors.RESET))
                if target:
                    self.run_nmap_scan(target, ["-F", "-T4", "-sV", "--top-ports", "100"])
            elif choice == 'f':
                target = input(self.center(Colors.CYAN + 'Enter target IP/Domain: ' + Colors.RESET))
                if target:
                    confirm = input(self.center(Colors.RED + 'Full scan may take minutes. Continue? (y/n): ' + Colors.RESET))
                    if confirm.lower() == 'y':
                        self.run_nmap_scan(target, ["-sS", "-sV", "-sC", "-O", "-T4", "-p-"])
            elif choice == 'd':
                target = input(self.center(Colors.CYAN + 'Enter domain for DNS recon: ' + Colors.RESET))
                if target:
                    self.run_nmap_scan(target, ["-sS", "-sV", "-sC", "-T4", "-p", "53"])
            elif choice == 'h':
                self.show_help()
                input(self.center(Colors.DIM + 'Press Enter...' + Colors.RESET))
            else:
                if choice:
                    print(self.center(Colors.RED + '[!] Unknown command' + Colors.RESET))
                    time.sleep(1)
    
    def show_help(self):
        help_text = f"""
{self.center(Colors.CYAN + '═' * 60 + Colors.RESET)}
{self.center(Colors.GREEN + '🛡️ DSTERMINAL SOC DASHBOARD HELP' + Colors.RESET)}
{self.center(Colors.CYAN + '═' * 60 + Colors.RESET)}
{self.center(Colors.YELLOW + 'Commands:' + Colors.RESET)}
{self.center(Colors.GREEN + '  [S] - Standard Scan' + Colors.RESET)}
{self.center(Colors.GREEN + '  [Q] - Quick Scan' + Colors.RESET)}
{self.center(Colors.GREEN + '  [F] - Full Scan' + Colors.RESET)}
{self.center(Colors.GREEN + '  [D] - DNS Reconnaissance' + Colors.RESET)}
{self.center(Colors.GREEN + '  [H] - Help' + Colors.RESET)}
{self.center(Colors.GREEN + '  [X] - Exit' + Colors.RESET)}
{self.center(Colors.CYAN + '═' * 60 + Colors.RESET)}
"""
        print(help_text)

# ============================================================
# EXPORTED CLASSES FOR MAIN DSTERMINAL
# ============================================================

# These are the classes that will be imported by dsterminal.py
__all__ = ['InteractiveSOCDashboard', 'SOCNmapDashboard', 'SOCNmapIntegration']

# Alias for backward compatibility - THIS IS CRITICAL
SOCNmapDashboard = InteractiveSOCDashboard

class SOCNmapIntegration:
    def __init__(self):
        self.dashboard = None
    
    def start_interactive_dashboard(self):
        if not self.dashboard:
            self.dashboard = InteractiveSOCDashboard()
        self.dashboard.interactive_loop()
    
    def quick_scan(self, target: str):
        if not self.dashboard:
            self.dashboard = InteractiveSOCDashboard()
        print(f"[+] Running quick scan on {target}")
        self.dashboard.run_nmap_scan(target, ["-F", "-T4", "-sV", "--top-ports", "100"])
        self.dashboard.generate_full_dashboard()
    
    def standard_scan(self, target: str):
        if not self.dashboard:
            self.dashboard = InteractiveSOCDashboard()
        print(f"[+] Running standard scan on {target}")
        self.dashboard.run_nmap_scan(target, ["-sS", "-sV", "-T4"])
        self.dashboard.generate_full_dashboard()
    
    def full_scan(self, target: str):
        if not self.dashboard:
            self.dashboard = InteractiveSOCDashboard()
        print(f"[+] Running full scan on {target}")
        self.dashboard.run_nmap_scan(target, ["-sS", "-sV", "-sC", "-O", "-T4", "-p-"])
        self.dashboard.generate_full_dashboard()
    
    def dns_recon(self, target: str):
        if not self.dashboard:
            self.dashboard = InteractiveSOCDashboard()
        print(f"[+] Running DNS recon on {target}")
        self.dashboard.run_nmap_scan(target, ["-sS", "-sV", "-sC", "-T4", "-p", "53"])
        self.dashboard.generate_full_dashboard()


# ============================================================
# MAIN ENTRY POINT (for standalone execution)
# ============================================================

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"{' '*15}DSTERMINAL SOC NMAP DASHBOARD")
    print(f"{'='*60}\n")
    soc = SOCNmapIntegration()
    soc.start_interactive_dashboard()
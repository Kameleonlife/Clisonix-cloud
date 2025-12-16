"""
📊 SPECTRUM ANALYZER API ROUTES
FastAPI endpoints for industrial-grade spectrum analysis
Real-time FFT processing and frequency visualization
"""

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import numpy as np
import json
import asyncio
import logging
from datetime import datetime

# Import spectrum analyzer
try:
    from app.services.spectrum_analyzer import spectrum_analyzer, FrequencyBand
except ImportError:
    from ..services.spectrum_analyzer import spectrum_analyzer, FrequencyBand

logger = logging.getLogger("SpectrumAnalyzer-API")

# Create router
router = APIRouter(prefix="/spectrum", tags=["Spectrum Analyzer"])

# WebSocket connections for real-time updates
active_connections: List[WebSocket] = []

# Pydantic models
class AnalysisRequest(BaseModel):
    channel: str
    signal_data: List[float]
    fft_size: Optional[int] = 512
    window_function: Optional[str] = "hanning"

class MultiChannelAnalysisRequest(BaseModel):
    channels: Dict[str, List[float]]
    analysis_type: Optional[str] = "spectrum"  # "spectrum", "coherence", "comparative"

class AnalysisConfigRequest(BaseModel):
    sampling_rate: Optional[int] = 250
    fft_size: Optional[int] = 512
    window_function: Optional[str] = "hanning"
    overlap: Optional[float] = 0.5
    max_frequency: Optional[float] = 100.0

@router.get("/status")
async def get_analyzer_status():
    """Get spectrum analyzer status and performance metrics"""
    try:
        performance = spectrum_analyzer.get_performance_metrics()
        
        return {
            "status": "operational",
            "analyzer_config": {
                "sampling_rate": spectrum_analyzer.sampling_rate,
                "fft_size": spectrum_analyzer.fft_size,
                "window_function": spectrum_analyzer.window_function,
                "overlap": spectrum_analyzer.overlap,
                "max_frequency": spectrum_analyzer.max_frequency,
                "frequency_resolution": spectrum_analyzer.frequency_resolution
            },
            "frequency_bands": {
                name: {
                    "name": band.name,
                    "range": band.frequency_range,
                    "color": band.color
                }
                for name, band in spectrum_analyzer.frequency_bands.items()
            },
            "performance_metrics": performance,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Status error: {e}")
        raise HTTPException(status_code=500, detail=f"Status retrieval failed: {str(e)}")

@router.post("/analyze")
async def analyze_single_channel(request: AnalysisRequest):
    """Analyze spectrum for a single channel"""
    try:
        # Convert signal data to numpy array
        signal_data = np.array(request.signal_data)
        
        # Perform analysis
        result = await spectrum_analyzer.analyze_spectrum(
            channel=request.channel,
            signal_data=signal_data
        )
        
        return {
            "success": True,
            "analysis": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Single channel analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/analyze-multichannel")
async def analyze_multiple_channels(request: MultiChannelAnalysisRequest):
    """Analyze spectrum for multiple channels"""
    try:
        results = {}
        
        # Analyze each channel
        for channel, signal_data in request.channels.items():
            signal_array = np.array(signal_data)
            analysis_result = await spectrum_analyzer.analyze_spectrum(
                channel=channel,
                signal_data=signal_array
            )
            results[channel] = analysis_result
        
        # Perform coherence analysis if requested
        coherence_analysis = None
        if request.analysis_type == "coherence" and len(request.channels) >= 2:
            channel_data = {
                channel: np.array(data) 
                for channel, data in request.channels.items()
            }
            coherence_analysis = await spectrum_analyzer.analyze_coherence(channel_data)
        
        return {
            "success": True,
            "analysis_type": request.analysis_type,
            "channel_analyses": results,
            "coherence_analysis": coherence_analysis.__dict__ if coherence_analysis else None,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Multi-channel analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Multi-channel analysis failed: {str(e)}")

@router.post("/add-data")
async def add_signal_data(channel: str, data: List[float]):
    """Add signal data to real-time processing buffer"""
    try:
        signal_array = np.array(data)
        spectrum_analyzer.add_signal_data(channel, signal_array)
        
        return {
            "success": True,
            "channel": channel,
            "samples_added": len(data),
            "buffer_size": len(spectrum_analyzer.signal_buffers.get(channel, [])),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Add data error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to add data: {str(e)}")

@router.get("/history/{channel}")
async def get_analysis_history(channel: str, limit: int = 100):
    """Get historical analysis data for a channel"""
    try:
        history = spectrum_analyzer.get_analysis_history(channel, limit)
        
        return {
            "success": True,
            "channel": channel,
            "history": history,
            "count": len(history),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"History retrieval error: {e}")
        raise HTTPException(status_code=500, detail=f"History retrieval failed: {str(e)}")

@router.get("/frequency-bands")
async def get_frequency_bands():
    """Get standard EEG frequency band definitions"""
    try:
        bands = {}
        for name, band in spectrum_analyzer.frequency_bands.items():
            bands[name] = {
                "name": band.name,
                "frequency_range": band.frequency_range,
                "color": band.color,
                "description": f"{band.frequency_range[0]}-{band.frequency_range[1]} Hz"
            }
        
        return {
            "success": True,
            "frequency_bands": bands,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Frequency bands error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get frequency bands: {str(e)}")

@router.post("/configure")
async def configure_analyzer(config: AnalysisConfigRequest):
    """Configure spectrum analyzer parameters"""
    try:
        # Create new analyzer with updated configuration
        from app.services.spectrum_analyzer import IndustrialSpectrumAnalyzer
        
        new_analyzer = IndustrialSpectrumAnalyzer(
            sampling_rate=config.sampling_rate,
            fft_size=config.fft_size,
            window_function=config.window_function,
            overlap=config.overlap,
            max_frequency=config.max_frequency
        )
        
        # Replace global analyzer (in production, this should be handled more carefully)
        spectrum_analyzer.__dict__.update(new_analyzer.__dict__)
        
        return {
            "success": True,
            "message": "Analyzer configuration updated",
            "new_config": {
                "sampling_rate": spectrum_analyzer.sampling_rate,
                "fft_size": spectrum_analyzer.fft_size,
                "window_function": spectrum_analyzer.window_function,
                "overlap": spectrum_analyzer.overlap,
                "max_frequency": spectrum_analyzer.max_frequency
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Configuration error: {e}")
        raise HTTPException(status_code=500, detail=f"Configuration failed: {str(e)}")

@router.post("/reset")
async def reset_analyzer():
    """Reset analyzer state and clear all buffers"""
    try:
        spectrum_analyzer.reset_analyzer()
        
        return {
            "success": True,
            "message": "Spectrum analyzer reset completed",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Reset error: {e}")
        raise HTTPException(status_code=500, detail=f"Reset failed: {str(e)}")

@router.get("/export/{channel}")
async def export_analysis_data(channel: str, format: str = "json"):
    """Export analysis data in various formats"""
    try:
        # Get analysis history
        history = spectrum_analyzer.get_analysis_history(channel, limit=0)  # All data
        
        if format.lower() == "json":
            return {
                "success": True,
                "channel": channel,
                "format": "json",
                "data": history,
                "export_timestamp": datetime.utcnow().isoformat()
            }
        elif format.lower() == "csv":
            # Convert to CSV format (simplified)
            csv_data = []
            for entry in history:
                csv_data.append({
                    "timestamp": entry["timestamp"],
                    "dominant_frequency": entry["dominant_frequency"],
                    "total_power": entry["total_power"],
                    "quality_score": entry["quality_score"]
                })
            
            return {
                "success": True,
                "channel": channel,
                "format": "csv",
                "data": csv_data,
                "export_timestamp": datetime.utcnow().isoformat()
            }
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported format: {format}")
        
    except Exception as e:
        logger.error(f"Export error: {e}")
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

# WebSocket endpoint for real-time spectrum updates
@router.websocket("/realtime")
async def websocket_realtime_spectrum(websocket: WebSocket):
    """WebSocket endpoint for real-time spectrum analysis updates"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            # Wait for client data
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "analyze":
                # Perform real-time analysis
                channel = message.get("channel", "default")
                signal_data = np.array(message.get("signal_data", []))
                
                if len(signal_data) > 0:
                    # Add to buffer for continuous analysis
                    spectrum_analyzer.add_signal_data(channel, signal_data)
                    
                    # Perform analysis
                    result = await spectrum_analyzer.analyze_spectrum(channel)
                    
                    # Send result back
                    await websocket.send_text(json.dumps({
                        "type": "analysis_result",
                        "channel": channel,
                        "result": result,
                        "timestamp": datetime.utcnow().isoformat()
                    }))
            
            elif message.get("type") == "get_status":
                # Send status update
                performance = spectrum_analyzer.get_performance_metrics()
                await websocket.send_text(json.dumps({
                    "type": "status_update",
                    "performance": performance,
                    "timestamp": datetime.utcnow().isoformat()
                }))
            
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        if websocket in active_connections:
            active_connections.remove(websocket)

# Utility function to broadcast updates to all connected clients
async def broadcast_spectrum_update(channel: str, analysis_result: Dict[str, Any]):
    """Broadcast spectrum analysis update to all connected WebSocket clients"""
    if not active_connections:
        return
    
    message = {
        "type": "spectrum_update",
        "channel": channel,
        "analysis": analysis_result,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Send to all connected clients
    disconnected = []
    for connection in active_connections:
        try:
            await connection.send_text(json.dumps(message))
        except:
            disconnected.append(connection)
    
    # Remove disconnected clients
    for connection in disconnected:
        active_connections.remove(connection)

# Health check endpoint
@router.get("/health")
async def health_check():
    """Health check endpoint for spectrum analyzer service"""
    return {
        "status": "healthy",
        "service": "spectrum_analyzer",
        "timestamp": datetime.utcnow().isoformat(),
        "analyzer_operational": True,
        "active_websockets": len(active_connections)
    }



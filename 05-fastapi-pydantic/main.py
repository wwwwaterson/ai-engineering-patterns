"""
Space Mission Control API

A demonstration FastAPI application showcasing:
- RESTful API design with FastAPI
- Pydantic data validation
- In-memory data storage (for demo purposes)
- Comprehensive error handling
- Auto-generated interactive documentation

Run with: uvicorn main:app --reload
Access docs at: http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List, Dict
from models import (
    Astronaut, 
    Mission, 
    CrewAssignment, 
    AstronautResponse, 
    MissionResponse
)

# Initialize FastAPI application
app = FastAPI(
    title="Space Mission Control API",
    description="A fun demonstration of Pydantic validation and FastAPI routing",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# In-memory storage (in production, use a real database)
astronauts_db: Dict[int, Astronaut] = {}
missions_db: Dict[int, Mission] = {}
crew_assignments: List[Dict] = []

# Auto-incrementing ID counters
astronaut_id_counter = 1
mission_id_counter = 1


@app.get("/", tags=["Root"])
async def root():
    """
    Welcome endpoint with API information.
    
    Returns basic information about the API and available endpoints.
    """
    return {
        "message": "Welcome to Space Mission Control API! 🚀",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "astronauts": "/astronauts/",
            "missions": "/missions/"
        }
    }


# ============================================================================
# ASTRONAUT ENDPOINTS
# ============================================================================

@app.post(
    "/astronauts/", 
    response_model=AstronautResponse, 
    status_code=status.HTTP_201_CREATED,
    tags=["Astronauts"]
)
async def create_astronaut(astronaut: Astronaut):
    """
    Register a new astronaut in the space program.
    
    This endpoint demonstrates:
    - Automatic Pydantic validation of incoming data
    - Custom validators (age, experience, name format)
    - Email validation
    - Response model serialization
    
    Args:
        astronaut: Astronaut data (validated by Pydantic)
    
    Returns:
        The created astronaut with assigned ID
    
    Raises:
        422: Validation error if data doesn't meet requirements
    """
    global astronaut_id_counter
    
    # Assign a unique ID
    astronaut.id = astronaut_id_counter
    astronaut_id_counter += 1
    
    # Store in our "database"
    astronauts_db[astronaut.id] = astronaut
    
    return astronaut


@app.get(
    "/astronauts/", 
    response_model=List[AstronautResponse],
    tags=["Astronauts"]
)
async def list_astronauts(
    active_only: bool = False,
    specialization: str = None
):
    """
    List all registered astronauts.
    
    Query parameters allow filtering:
    - active_only: Show only active astronauts
    - specialization: Filter by specialization
    
    Args:
        active_only: If True, only return active astronauts
        specialization: Filter by astronaut specialization
    
    Returns:
        List of astronauts matching the criteria
    """
    astronauts = list(astronauts_db.values())
    
    # Apply filters
    if active_only:
        astronauts = [a for a in astronauts if a.active]
    
    if specialization:
        astronauts = [a for a in astronauts if a.specialization == specialization]
    
    return astronauts


@app.get(
    "/astronauts/{astronaut_id}", 
    response_model=AstronautResponse,
    tags=["Astronauts"]
)
async def get_astronaut(astronaut_id: int):
    """
    Get details of a specific astronaut.
    
    Args:
        astronaut_id: The unique identifier of the astronaut
    
    Returns:
        Astronaut details
    
    Raises:
        404: If astronaut not found
    """
    if astronaut_id not in astronauts_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Astronaut with ID {astronaut_id} not found"
        )
    
    return astronauts_db[astronaut_id]


@app.put(
    "/astronauts/{astronaut_id}",
    response_model=AstronautResponse,
    tags=["Astronauts"]
)
async def update_astronaut(astronaut_id: int, astronaut_update: Astronaut):
    """
    Update an existing astronaut's information.
    
    Args:
        astronaut_id: The unique identifier of the astronaut
        astronaut_update: Updated astronaut data
    
    Returns:
        Updated astronaut details
    
    Raises:
        404: If astronaut not found
    """
    if astronaut_id not in astronauts_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Astronaut with ID {astronaut_id} not found"
        )
    
    # Preserve the ID
    astronaut_update.id = astronaut_id
    astronauts_db[astronaut_id] = astronaut_update
    
    return astronaut_update


@app.delete(
    "/astronauts/{astronaut_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Astronauts"]
)
async def delete_astronaut(astronaut_id: int):
    """
    Remove an astronaut from the program.
    
    Args:
        astronaut_id: The unique identifier of the astronaut
    
    Raises:
        404: If astronaut not found
    """
    if astronaut_id not in astronauts_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Astronaut with ID {astronaut_id} not found"
        )
    
    del astronauts_db[astronaut_id]
    return None


# ============================================================================
# MISSION ENDPOINTS
# ============================================================================

@app.post(
    "/missions/", 
    response_model=MissionResponse, 
    status_code=status.HTTP_201_CREATED,
    tags=["Missions"]
)
async def create_mission(mission: Mission):
    """
    Create a new space mission.
    
    This endpoint demonstrates:
    - Validation of mission parameters (duration, crew capacity)
    - Date validation (launch date must be in future)
    - Status management
    
    Args:
        mission: Mission data (validated by Pydantic)
    
    Returns:
        The created mission with assigned ID
    
    Raises:
        422: Validation error if data doesn't meet requirements
    """
    global mission_id_counter
    
    # Assign a unique ID
    mission.id = mission_id_counter
    mission_id_counter += 1
    
    # Store in our "database"
    missions_db[mission.id] = mission
    
    return mission


@app.get(
    "/missions/", 
    response_model=List[MissionResponse],
    tags=["Missions"]
)
async def list_missions(status_filter: str = None):
    """
    List all missions.
    
    Query parameters allow filtering:
    - status: Filter by mission status
    
    Args:
        status_filter: Filter by mission status (planning, active, completed, cancelled)
    
    Returns:
        List of missions matching the criteria
    """
    missions = list(missions_db.values())
    
    # Apply status filter
    if status_filter:
        missions = [m for m in missions if m.status == status_filter]
    
    return missions


@app.get(
    "/missions/{mission_id}", 
    response_model=MissionResponse,
    tags=["Missions"]
)
async def get_mission(mission_id: int):
    """
    Get details of a specific mission.
    
    Args:
        mission_id: The unique identifier of the mission
    
    Returns:
        Mission details
    
    Raises:
        404: If mission not found
    """
    if mission_id not in missions_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mission with ID {mission_id} not found"
        )
    
    return missions_db[mission_id]


@app.put(
    "/missions/{mission_id}",
    response_model=MissionResponse,
    tags=["Missions"]
)
async def update_mission(mission_id: int, mission_update: Mission):
    """
    Update an existing mission's information.
    
    Args:
        mission_id: The unique identifier of the mission
        mission_update: Updated mission data
    
    Returns:
        Updated mission details
    
    Raises:
        404: If mission not found
    """
    if mission_id not in missions_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mission with ID {mission_id} not found"
        )
    
    # Preserve the ID
    mission_update.id = mission_id
    missions_db[mission_id] = mission_update
    
    return mission_update


# ============================================================================
# CREW ASSIGNMENT ENDPOINTS
# ============================================================================

@app.post(
    "/missions/{mission_id}/assign",
    status_code=status.HTTP_200_OK,
    tags=["Crew Assignments"]
)
async def assign_crew_to_mission(mission_id: int, assignment: CrewAssignment):
    """
    Assign an astronaut to a mission.
    
    This endpoint demonstrates:
    - Cross-model validation
    - Business logic enforcement
    - Error handling for invalid operations
    
    Args:
        mission_id: The mission ID (must match assignment.mission_id)
        assignment: Crew assignment details
    
    Returns:
        Success message with assignment details
    
    Raises:
        400: If mission_id doesn't match or validation fails
        404: If astronaut or mission not found
    """
    # Validate mission_id matches
    if mission_id != assignment.mission_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mission ID in URL doesn't match assignment data"
        )
    
    # Check if mission exists
    if mission_id not in missions_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mission with ID {mission_id} not found"
        )
    
    # Check if astronaut exists
    if assignment.astronaut_id not in astronauts_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Astronaut with ID {assignment.astronaut_id} not found"
        )
    
    mission = missions_db[mission_id]
    astronaut = astronauts_db[assignment.astronaut_id]
    
    # Check if astronaut is active
    if not astronaut.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Astronaut {astronaut.name} is not active"
        )
    
    # Check if mission has capacity
    if mission.current_crew_count >= mission.crew_capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Mission {mission.name} is at full capacity"
        )
    
    # Check if astronaut is already assigned to this mission
    for existing_assignment in crew_assignments:
        if (existing_assignment["astronaut_id"] == assignment.astronaut_id and 
            existing_assignment["mission_id"] == mission_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Astronaut {astronaut.name} is already assigned to this mission"
            )
    
    # Create the assignment
    crew_assignments.append({
        "astronaut_id": assignment.astronaut_id,
        "mission_id": mission_id,
        "role": assignment.role,
        "astronaut_name": astronaut.name,
        "mission_name": mission.name
    })
    
    # Update mission crew count
    mission.current_crew_count += 1
    
    return {
        "message": "Crew assignment successful! 🚀",
        "astronaut": astronaut.name,
        "mission": mission.name,
        "role": assignment.role,
        "crew_count": f"{mission.current_crew_count}/{mission.crew_capacity}"
    }


@app.get(
    "/missions/{mission_id}/crew",
    tags=["Crew Assignments"]
)
async def get_mission_crew(mission_id: int):
    """
    Get all crew members assigned to a mission.
    
    Args:
        mission_id: The unique identifier of the mission
    
    Returns:
        List of crew assignments for the mission
    
    Raises:
        404: If mission not found
    """
    if mission_id not in missions_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mission with ID {mission_id} not found"
        )
    
    mission_crew = [
        assignment for assignment in crew_assignments 
        if assignment["mission_id"] == mission_id
    ]
    
    return {
        "mission": missions_db[mission_id].name,
        "crew_count": len(mission_crew),
        "crew_members": mission_crew
    }


@app.get(
    "/astronauts/{astronaut_id}/missions",
    tags=["Crew Assignments"]
)
async def get_astronaut_missions(astronaut_id: int):
    """
    Get all missions assigned to an astronaut.
    
    Args:
        astronaut_id: The unique identifier of the astronaut
    
    Returns:
        List of mission assignments for the astronaut
    
    Raises:
        404: If astronaut not found
    """
    if astronaut_id not in astronauts_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Astronaut with ID {astronaut_id} not found"
        )
    
    astronaut_missions = [
        assignment for assignment in crew_assignments 
        if assignment["astronaut_id"] == astronaut_id
    ]
    
    return {
        "astronaut": astronauts_db[astronaut_id].name,
        "mission_count": len(astronaut_missions),
        "missions": astronaut_missions
    }


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/health", tags=["System"])
async def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns:
        System status and statistics
    """
    return {
        "status": "healthy",
        "astronauts_count": len(astronauts_db),
        "missions_count": len(missions_db),
        "crew_assignments_count": len(crew_assignments)
    }

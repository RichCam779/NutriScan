from fastapi import APIRouter, HTTPException
from controllers.user_controller import UserController
from models.user_model import User, BiotypeUpdate
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

user_controller = UserController()

@router.post("/", response_model=dict)
def create_user(user: User):
    return user_controller.create_user(user)

@router.get("/", response_model=dict)
def get_active_users():
    return user_controller.get_active_users()

@router.put("/{user_id}", response_model=dict)
def update_user(user_id: int, user: User):
    # Ensure the user object has the ID from the path if needed, 
    # or just pass it as is depending on controller logic.
    # The controller's update_user uses user.id, so we should set it.
    user.id = user_id
    return user_controller.update_user(user)

@router.delete("/{user_id}", response_model=dict)
def deactivate_user(user_id: int):
    return user_controller.deactivate_user(user_id)

# Ejemplo corregido usando el modelo de Pydantic
@router.put("/{user_id}/biotype")
def update_biotype(user_id: int, data: BiotypeUpdate): 
    return user_controller.update_biotype(user_id, data.biotipo, data.confianza_ia)

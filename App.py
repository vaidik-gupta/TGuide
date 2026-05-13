from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from TerminalRegistry import TerminalRegistry


class StatusResponse(BaseModel):
    status: str


class TerminalRegistration(BaseModel):
    terminal_id: str
    fd: int


class TerminalStatusResponse(BaseModel):
    status: str
    temp_path: str


app = FastAPI()
registry = TerminalRegistry()


@app.get("/", response_model=StatusResponse)
def status():
    return StatusResponse(status="ok")


@app.post("/terminal", response_model=TerminalStatusResponse)
def register_terminal(registration: TerminalRegistration):
    try:
        temp_path = registry.register(registration.terminal_id, registration.fd)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return TerminalStatusResponse(status="registered", temp_path=temp_path)


@app.delete("/terminal/{terminal_id}", response_model=StatusResponse)
def deregister_terminal(terminal_id: str):
    try:
        registry.deregister(terminal_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Terminal not registered")

    return StatusResponse(status="deregistered")

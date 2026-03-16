#!/usr/bin/env python3
"""CQRS — Command Query Responsibility Segregation."""
import sys, copy

class Command:
    def __init__(self, type, data): self.type = type; self.data = data

class CommandBus:
    def __init__(self): self.handlers = {}
    def register(self, cmd_type, handler): self.handlers[cmd_type] = handler
    def dispatch(self, cmd):
        if cmd.type not in self.handlers: raise ValueError(f"No handler for {cmd.type}")
        return self.handlers[cmd.type](cmd)

class ReadModel:
    def __init__(self): self.data = {}
    def project(self, event_type, data):
        if event_type == "UserCreated": self.data[data["id"]] = {"name": data["name"], "email": data["email"], "orders": 0}
        elif event_type == "OrderPlaced":
            uid = data["user_id"]
            if uid in self.data: self.data[uid]["orders"] += 1
    def query(self, user_id): return self.data.get(user_id)
    def list_all(self): return list(self.data.values())

if __name__ == "__main__":
    events = []; read = ReadModel()
    bus = CommandBus()
    def create_user(cmd):
        e = ("UserCreated", cmd.data); events.append(e); read.project(*e); return e
    def place_order(cmd):
        e = ("OrderPlaced", cmd.data); events.append(e); read.project(*e); return e
    bus.register("CreateUser", create_user)
    bus.register("PlaceOrder", place_order)
    bus.dispatch(Command("CreateUser", {"id": "u1", "name": "Alice", "email": "a@b.com"}))
    bus.dispatch(Command("PlaceOrder", {"user_id": "u1", "item": "widget"}))
    bus.dispatch(Command("PlaceOrder", {"user_id": "u1", "item": "gadget"}))
    print(f"User u1: {read.query('u1')}")
    print(f"Events: {len(events)}")

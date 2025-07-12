import streamlit as st

class AppState:
    _state = {
        "vendor_code": "",
        "name": "",
        "transactions": 0.0,
        "income1": 0.0,
        "income2": 0.0,
        "income3": 0.0,
        "expense1": 0.0,
        "expense2": 0.0,
        "expense3": 0.0,
        "submitted": False
    }

    @classmethod
    def get(cls, key):
        return cls._state.get(key, None)

    @classmethod
    def set(cls, key, value):
        cls._state[key] = value

    @classmethod
    def reset(cls):
        for key in cls._state:
            if isinstance(cls._state[key], (int, float)):
                cls._state[key] = 0.0
            elif isinstance(cls._state[key], bool):
                cls._state[key] = False
            else:
                cls._state[key] = ""

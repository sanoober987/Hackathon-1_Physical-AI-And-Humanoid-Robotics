from typing import Dict
import time
from datetime import datetime, timedelta
import asyncio

class RateLimiter:
    def __init__(self):
        # Dictionary to store request counts per user
        # Format: {user_id: [(timestamp, count), ...]}
        self.requests = {}
        # Default rate limit: 100 requests per hour per user
        self.default_requests_per_hour = 100
        self.time_window_seconds = 3600  # 1 hour

    def is_allowed(self, user_id: str, max_requests: int = None) -> bool:
        """
        Check if the user is allowed to make a request
        """
        if max_requests is None:
            max_requests = self.default_requests_per_hour

        current_time = time.time()

        # Clean old requests outside the time window
        self._clean_old_requests(user_id, current_time)

        # Get user's request history
        user_requests = self.requests.get(user_id, [])

        # Check if user has exceeded the limit
        if len(user_requests) >= max_requests:
            return False

        # Add current request to history
        self.requests.setdefault(user_id, []).append(current_time)

        return True

    def get_remaining_requests(self, user_id: str, max_requests: int = None) -> int:
        """
        Get the number of remaining requests for the user in the current window
        """
        if max_requests is None:
            max_requests = self.default_requests_per_hour

        current_time = time.time()
        self._clean_old_requests(user_id, current_time)

        user_requests = self.requests.get(user_id, [])
        return max(max_requests - len(user_requests), 0)

    def get_reset_time(self, user_id: str) -> float:
        """
        Get the time when the rate limit will reset for the user
        """
        user_requests = self.requests.get(user_id, [])
        if not user_requests:
            return time.time()

        # Reset time is 1 hour after the oldest request in the window
        oldest_request = min(user_requests)
        reset_time = oldest_request + self.time_window_seconds
        return reset_time

    def _clean_old_requests(self, user_id: str, current_time: float):
        """
        Remove requests older than the time window
        """
        if user_id not in self.requests:
            return

        # Keep only requests within the time window
        recent_requests = [
            req_time for req_time in self.requests[user_id]
            if current_time - req_time <= self.time_window_seconds
        ]
        self.requests[user_id] = recent_requests

    def set_rate_limit(self, user_id: str, max_requests: int, time_window_hours: int = 1):
        """
        Set a custom rate limit for a specific user
        """
        self.default_requests_per_hour = max_requests
        self.time_window_seconds = time_window_hours * 3600

class GlobalRateLimiter:
    def __init__(self):
        self.global_requests = []
        self.global_limit = 1000  # 1000 requests per hour globally
        self.time_window_seconds = 3600  # 1 hour

    def is_allowed(self) -> bool:
        """
        Check if global rate limit allows a new request
        """
        current_time = time.time()

        # Clean old requests outside the time window
        self.global_requests = [
            req_time for req_time in self.global_requests
            if current_time - req_time <= self.time_window_seconds
        ]

        # Check if global limit is exceeded
        if len(self.global_requests) >= self.global_limit:
            return False

        # Add current request
        self.global_requests.append(current_time)
        return True
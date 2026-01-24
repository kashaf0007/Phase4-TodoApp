"""
Performance monitoring and metrics utilities
"""
import time
import functools
import asyncio
from typing import Callable, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class MetricsCollector:
    """
    Collects and reports application metrics
    """
    def __init__(self):
        self.metrics = {}
    
    def record_timing(self, metric_name: str, duration: float):
        """Record a timing metric"""
        if metric_name not in self.metrics:
            self.metrics[metric_name] = []
        self.metrics[metric_name].append(duration)
    
    def get_average(self, metric_name: str) -> float:
        """Get average value for a metric"""
        if metric_name in self.metrics and self.metrics[metric_name]:
            values = self.metrics[metric_name]
            return sum(values) / len(values)
        return 0.0
    
    def get_count(self, metric_name: str) -> int:
        """Get count of recorded values for a metric"""
        return len(self.metrics.get(metric_name, []))
    
    def reset_metrics(self):
        """Reset all collected metrics"""
        self.metrics = {}

# Global metrics collector instance
metrics_collector = MetricsCollector()

def time_it(metric_name: str):
    """
    Decorator to time function execution and record metrics
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start_time
                metrics_collector.record_timing(metric_name, duration)
                logger.debug(f"{metric_name} took {duration:.4f}s")
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start_time
                metrics_collector.record_timing(metric_name, duration)
                logger.debug(f"{metric_name} took {duration:.4f}s")
        
        # Return the appropriate wrapper based on whether the function is async
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator

def log_performance_stats():
    """
    Log current performance statistics
    """
    for metric_name in metrics_collector.metrics:
        avg_time = metrics_collector.get_average(metric_name)
        count = metrics_collector.get_count(metric_name)
        logger.info(f"Performance stats for {metric_name}: avg={avg_time:.4f}s, count={count}")

# For backward compatibility
def monitor_performance(func: Callable) -> Callable:
    """
    Decorator to monitor performance of functions
    """
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            duration = time.time() - start_time
            logger.info(f"{func.__name__} executed in {duration:.4f} seconds")
    
    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            duration = time.time() - start_time
            logger.info(f"{func.__name__} executed in {duration:.4f} seconds")
    
    # Return the appropriate wrapper based on whether the function is async
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper
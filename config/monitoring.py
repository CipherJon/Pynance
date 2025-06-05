from prometheus_flask_exporter import PrometheusMetrics
import logging

logger = logging.getLogger(__name__)

# Initialize Prometheus metrics as None
metrics = None

def init_monitoring(app):
    """Initialize monitoring with the Flask app."""
    global metrics
    try:
        # Initialize metrics with app
        metrics = PrometheusMetrics(app)
        
        # Add default metrics
        metrics.info('app_info', 'Application info', version='1.0.0')
        
        # Add custom metrics
        metrics.register_default(
            metrics.counter(
                'by_path_counter', 'Request count by request paths',
                labels={'path': lambda: request.path}
            )
        )
        
        # Add endpoint metrics
        metrics.register_default(
            metrics.histogram(
                'by_path_latency_seconds', 'Request latency by request paths',
                labels={'path': lambda: request.path}
            )
        )
        
        logger.info("Monitoring initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize monitoring: {e}")
        raise 
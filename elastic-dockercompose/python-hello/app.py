import os
import logging

from flask import Flask, jsonify
from elasticapm.contrib.flask import ElasticAPM

app = Flask(__name__)

# --- Elastic APM configuration ---
# All values can be overridden via environment variables (see docker-compose.yml)
app.config['ELASTIC_APM'] = {
    'SERVICE_NAME': os.environ.get('ELASTIC_APM_SERVICE_NAME', 'hello-world-python'),
    'SERVER_URL': os.environ.get('ELASTIC_APM_SERVER_URL', 'http://100.61.19.183:8200'),
    'ENVIRONMENT': os.environ.get('ELASTIC_APM_ENVIRONMENT', 'development'),
    'SECRET_TOKEN': os.environ.get('ELASTIC_APM_SECRET_TOKEN', ''),
    'DEBUG': True,  # allow APM to run even when Flask debug=True
}

apm = ElasticAPM(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/')
def hello_world():
    logger.info('Handling request to /')
    return jsonify(message='Hello, World!')


@app.route('/health')
def health():
    return jsonify(status='ok')


@app.route('/error')
def trigger_error():
    """Intentionally raises an exception so you can see it captured in APM."""
    raise ValueError('This is a test error for APM to capture')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

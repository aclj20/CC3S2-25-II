import logging
import os
import random
import time

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor


LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("demo-app")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

file_handler = logging.FileHandler(os.path.join(LOG_DIR, "app.log"))
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

#  OpenTelemetry controlado SOLO por DISABLE_OTEL

DISABLE_OTEL = os.getenv("DISABLE_OTEL", "0") == "1"
provider = None
meter_provider = None

if not DISABLE_OTEL:
    # Configuración de recursos
    resource = Resource.create(
        {
            SERVICE_NAME: os.getenv("OTEL_SERVICE_NAME", "demo-app"),
            "service.namespace": "devsecops-demo",
            "deployment.environment": os.getenv("ENV", "development"),
        }
    )
    
    # Configuración de Traces
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    # Configuración de Metrics
    meter_provider = MeterProvider(
        resource=resource,
        metric_readers=[
            PeriodicExportingMetricReader(
                OTLPMetricExporter(
                    endpoint=f"{os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT', 'http://otel-collector:4318')}/v1/metrics"
                ),
                export_interval_millis=5000,
            )
        ]
    )
    metrics.set_meter_provider(meter_provider)

    # Configuración del endpoint OTLP
    otel_endpoint = os.getenv(
        "OTEL_EXPORTER_OTLP_ENDPOINT",
        "http://otel-collector:4318",
    ).rstrip("/")

    # Configuración del exportador de Traces
    span_exporter = OTLPSpanExporter(endpoint=f"{otel_endpoint}/v1/traces")
    span_processor = BatchSpanProcessor(span_exporter)
    provider.add_span_processor(span_processor)

# Inicialización de instrumentación
LoggingInstrumentor().instrument()

# Obtener tracers y métricas
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

# Definir métricas
http_request_counter = meter.create_counter(
    "http_requests_total",
    description="Total number of HTTP requests",
    unit="1",
)

http_request_duration = meter.create_histogram(
    "http_request_duration_seconds",
    description="Duration of HTTP requests in seconds",
    unit="s",
)

#  FastAPI

app = FastAPI(title="DevSecOps Observability Demo", version="0.1.0")

if provider is not None:
    FastAPIInstrumentor.instrument_app(app, tracer_provider=provider)
else:
    # Instrumentación con tracer provider por defecto (no-op)
    FastAPIInstrumentor.instrument_app(app)


class Item(BaseModel):
    id: int
    name: str
    price: float


ITEMS = [
    Item(id=1, name="widget", price=9.99),
    Item(id=2, name="gadget", price=19.99),
    Item(id=3, name="thing", price=3.50),
]


@app.get("/healthz")
async def healthz():
    start_time = time.time()
    logger.info("Health check OK")
    
    # Registrar métrica de duración
    duration = time.time() - start_time
    http_request_duration.record(
        duration,
        {"route": "/healthz", "method": "GET", "status_code": 200}
    )
    
    # Contador de solicitudes
    http_request_counter.add(1, {"route": "/healthz", "method": "GET", "status_code": 200})
    
    return {"status": "ok"}


@app.get("/api/v1/items")
async def list_items():
    start_time = time.time()
    with tracer.start_as_current_span("list_items") as span:
        try:
            logger.info("Listing items")
            time.sleep(random.uniform(0.01, 0.2))
            
            # Registrar métricas
            duration = time.time() - start_time
            http_request_duration.record(
                duration,
                {"route": "/api/v1/items", "method": "GET", "status_code": 200}
            )
            http_request_counter.add(1, {"route": "/api/v1/items", "method": "GET", "status_code": 200})
            
            return ITEMS
            
        except Exception as e:
            # Registrar error en las métricas
            http_request_counter.add(1, {"route": "/api/v1/items", "method": "GET", "status_code": 500})
            raise


@app.get("/api/v1/work")
async def do_work():
    start_time = time.time()
    with tracer.start_as_current_span("cpu_bound_work") as span:
        logger.info("Simulating CPU bound work")
        
        # Registrar métricas
        duration = time.time() - start_time
        http_request_duration.record(
            duration,
            {"route": "/api/v1/work", "method": "GET", "status_code": 200}
        )
        http_request_counter.add(1, {"route": "/api/v1/work", "method": "GET", "status_code": 200})
        total = 0
        for i in range(1, 100_000):
            total += i * i
        span.set_attribute("work.result", total)
        if random.random() < 0.2:
            logger.warning("Slow request simulated")
            time.sleep(0.5)
        return {"status": "done", "result": total}


@app.get("/api/v1/error")
async def error_endpoint():
    start_time = time.time()
    try:
        logger.error("Simulated error endpoint called")
        raise HTTPException(status_code=500, detail="Simulated error")
    except HTTPException as e:
        # Registrar métricas para errores
        duration = time.time() - start_time
        http_request_duration.record(
            duration,
            {"route": "/api/v1/error", "method": "GET", "status_code": 500}
        )
        http_request_counter.add(1, {"route": "/api/v1/error", "method": "GET", "status_code": 500})
        raise
    except Exception as e:
        # Registrar otros errores inesperados
        duration = time.time() - start_time
        http_request_duration.record(
            duration,
            {"route": "/api/v1/error", "method": "GET", "status_code": 500, "error": str(e)}
        )
        http_request_counter.add(1, {"route": "/api/v1/error", "method": "GET", "status_code": 500, "error": str(e)})
        raise


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)

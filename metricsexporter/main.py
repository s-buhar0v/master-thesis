from flask import Flask
from socialmonitor.dataextractors.vk import VkDataExtractor
from prometheus_client import generate_latest, CollectorRegistry, Gauge

REGISTRY = CollectorRegistry()

vk_data_extractor = VkDataExtractor()

posts_count_metric = Gauge(
    name='vk_group_posts_count',
    documentation='Current count of posts in the vk group',
    labelnames=['group'],
    registry=REGISTRY)

app = Flask(__name__)


@app.route("/metrics")
def metrics():
    posts_count = vk_data_extractor.get_group_posts_count(group_name='w220.club')
    posts_count_metric.labels(group='w220.club').set(posts_count)

    return generate_latest(REGISTRY), 200

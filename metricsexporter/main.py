from flask import Flask
from socialmonitor.dataextractors.vk import VkDataExtractor
from prometheus_client import generate_latest, CollectorRegistry, Gauge

REGISTRY = CollectorRegistry()

vk_data_extractor = VkDataExtractor()

vk_posts_count_metric = Gauge(
    name='vk_group_posts_count',
    documentation='Current count of posts in the vk group',
    labelnames=['group'],
    registry=REGISTRY)

vk_members_count_metric = Gauge(
    name='vk_group_members_count',
    documentation='Current count of members in the vk group',
    labelnames=['group'],
    registry=REGISTRY)

app = Flask(__name__)


@app.route("/metrics")
def metrics():
    posts_count = vk_data_extractor.get_group_posts_count(group_name='w220.club')
    members_count = vk_data_extractor.get_group_members_count(group_name='w220.club')

    vk_posts_count_metric.labels(group='w220.club').set(posts_count)
    vk_members_count_metric.labels(group='w220.club').set(members_count)

    return generate_latest(REGISTRY), 200

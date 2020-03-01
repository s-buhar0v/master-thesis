import pymongo
import os
from flask import Flask
from socialmonitor.dataproviders.vk import VkDataExtractor
from prometheus_client import generate_latest, CollectorRegistry, Gauge

REGISTRY = CollectorRegistry()
group_name = 'w220.club'

vk_data_extractor = VkDataExtractor()

metrics_exporter_up_metric = Gauge(
    name='metrics_exporter_up',
    documentation='metricsexporter web app status',
    labelnames=['container'],
    registry=REGISTRY)

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

vk_likes_count_metric = Gauge(
    name='vk_group_likes_count',
    documentation='Current count of post likes in the vk group',
    labelnames=['group'],
    registry=REGISTRY)

vk_comments_count_metric = Gauge(
    name='vk_group_comments_count',
    documentation='Current count of post comments in the vk group',
    labelnames=['group'],
    registry=REGISTRY)

vk_views_count_metric = Gauge(
    name='vk_group_views_count',
    documentation='Current count of post views in the vk group',
    labelnames=['group'],
    registry=REGISTRY)

vk_reposts_count_metric = Gauge(
    name='vk_group_reposts_count',
    documentation='Current count of reposts in the vk group',
    labelnames=['group'],
    registry=REGISTRY)

app = Flask(__name__)


@app.route("/metrics")
def metrics():
    client = pymongo.MongoClient(os.environ['MONGO_DB_CONNECTION_STRING'])
    db = client.masterthesis

    if db.metrics.count() > 0:
        likes_count = db.metrics.find_one({'group': group_name, 'metrics': 'likes'})['value']
        comments_count = db.metrics.find_one({'group': group_name, 'metrics': 'comments'})['value']
        views_count = db.metrics.find_one({'group': group_name, 'metrics': 'views'})['value']
        reposts_count = db.metrics.find_one({'group': group_name, 'metrics': 'reposts'})['value']

        posts_count = vk_data_extractor.get_group_posts_count(group_name=group_name)
        members_count = vk_data_extractor.get_group_members_count(group_name=group_name)

        vk_posts_count_metric.labels(group=group_name).set(posts_count)
        vk_members_count_metric.labels(group=group_name).set(members_count)

        vk_likes_count_metric.labels(group=group_name).set(likes_count)
        vk_comments_count_metric.labels(group=group_name).set(comments_count)
        vk_views_count_metric.labels(group=group_name).set(views_count)
        vk_reposts_count_metric.labels(group=group_name).set(reposts_count)

    metrics_exporter_up_metric.labels(container=os.environ['HOSTNAME']).set(1)

    return generate_latest(REGISTRY), 200

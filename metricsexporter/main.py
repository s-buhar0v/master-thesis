import pymongo
import os
from flask import Flask
from socialmonitor.dataproviders.vk import VkDataExtractor
from prometheus_client import generate_latest, CollectorRegistry, Gauge

REGISTRY = CollectorRegistry()

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
    groups = db.groups.find({})

    for g in groups:

        if db.metrics.count_documents({}) > 0:
            likes_count = db.metrics.find_one({'group': g['group'], 'metrics': 'likes'})['value']
            comments_count = db.metrics.find_one({'group': g['group'], 'metrics': 'comments'})['value']
            views_count = db.metrics.find_one({'group': g['group'], 'metrics': 'views'})['value']
            reposts_count = db.metrics.find_one({'group': g['group'], 'metrics': 'reposts'})['value']

            posts_count = vk_data_extractor.get_group_posts_count(group_name=g['group'])
            members_count = vk_data_extractor.get_group_members_count(group_name=g['group'])

            vk_posts_count_metric.labels(group=g['group']).set(posts_count)
            vk_members_count_metric.labels(group=g['group']).set(members_count)

            vk_likes_count_metric.labels(group=g['group']).set(likes_count)
            vk_comments_count_metric.labels(group=g['group']).set(comments_count)
            vk_views_count_metric.labels(group=g['group']).set(views_count)
            vk_reposts_count_metric.labels(group=g['group']).set(reposts_count)

    metrics_exporter_up_metric.labels(container=os.environ['HOSTNAME']).set(1)

    return generate_latest(REGISTRY), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')

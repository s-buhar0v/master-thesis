from flask import Flask, render_template

from socialmonitor.dataproviders.vk import VkDataExtractor

app = Flask(__name__)
vk_data_extractor = VkDataExtractor()


@app.route("/")
def home():
    print(vk_data_extractor.search_groups(keywords=['mercedes']))

    return render_template(template_name_or_list='index.html')

from flask import Flask, render_template, session, redirect, request


from socialmonitor.corelib.httpclient import HttpClientMixin

app = Flask(__name__, static_folder='static')

app.secret_key = b'\x9cf3\xf4\x1a!s\xca\xf9\xff\xf6\xac\x0fM\x1bl'
client_id = '6998234'
client_secret = 'PmBJJCcNxExSITw4AGpo'
redirect_uri = 'http://localhost:5001/authorize'

m = HttpClientMixin(api_base_url='https://oauth.vk.com')


@app.route('/analyze')
def analyze():
    return {}

# @app.route('/')
# def index():
#     access_token = session.get('access_token')
#
#     if access_token:
#         vk_data_extractor = VkDataExtractor(access_token=access_token)
#
#         print(vk_data_extractor.search_groups(keywords=['bmw']))
#         return render_template(template_name_or_list='index.html')
#     else:
#         code = request.args.get('code')
#         if not code:
#             return redirect(
#                 location=f'https://oauth.vk.com/authorize?client_id={client_id}&display=page&redirect_uri={redirect_uri}&scope=groups&response_type=code&v=5.103')
#         else:
#             return render_template(template_name_or_list='index.html')
#
#
# @app.route('/groups')
# def groups():
#     access_token = session.get('access_token')
#
#     if access_token:
#         vk_data_extractor = VkDataExtractor(access_token=access_token)
#
#         groups = vk_data_extractor.search_groups(keywords=['bmw'])
#
#         return render_template(template_name_or_list='index.html', groups=groups
#                                )
#     else:
#         return redirect(location='/')
#
#
# @app.route('/authorize')
# def main():
#     code = request.args['code']
#
#     session['access_token'] = m.request(
#         method='get',
#         endpoint=f'/access_token',
#         params={
#             'client_id': client_id,
#             'client_secret': client_secret,
#             'redirect_uri': redirect_uri,
#             'code': code
#         }).json()['access_token']
#
#     return redirect(location='/')

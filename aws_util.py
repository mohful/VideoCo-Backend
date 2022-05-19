# from flask import request, json, Response, current_app
# import boto3
# import traceback
# import json
# import time
# import urllib.request
# from jose import jwk, jwt
# from jose.utils import base64url_decode
# from functools import wraps
# import sys
# import traceback
# from app import app

# # Copyright 2017-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# #
# # Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file
# # except in compliance with the License. A copy of the License is located at
# #
# #     http://aws.amazon.com/apache2.0/
# #
# # or in the "license" file accompanying this file. This file is distributed on an "AS IS"
# # BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# # License for the specific language governing permissions and limitations under the License.

# region = app.config['AWS_REGION']
# userpool_id = app.config['AWS_USER_POOL_ID']
# app_client_id = app.config['AWS_APP_CLIENT_ID']
# keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region, userpool_id)
# # instead of re-downloading the public keys every time
# # we download them only on cold start
# # https://aws.amazon.com/blogs/compute/container-reuse-in-lambda/
# with urllib.request.urlopen(keys_url) as f:
#   response = f.read()
# keys = json.loads(response.decode('utf-8'))['keys']

# def lambda_handler(event, context=None):
#     token = event['token']
#     # get the kid from the headers prior to verification
#     headers = jwt.get_unverified_headers(token)
#     kid = headers['kid']
#     # search for the kid in the downloaded public keys
#     key_index = -1
#     for i in range(len(keys)):
#         if kid == keys[i]['kid']:
#             key_index = i
#             break
#     if key_index == -1:
#         return Response('Public key not found in jwks.json', status=403)
#         return False
#     # construct the public key
#     public_key = jwk.construct(keys[key_index])
#     # get the last two sections of the token,
#     # message and signature (encoded in base64)
#     message, encoded_signature = str(token).rsplit('.', 1)
#     # decode the signature
#     decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
#     # verify the signature
#     if not public_key.verify(message.encode("utf8"), decoded_signature):
#         return Response('Signature verification failed',status=403)
#         return False
#     print('Signature successfully verified')
#     # since we passed the verification, we can now safely
#     # use the unverified claims
#     claims = jwt.get_unverified_claims(token)
#     # additionally we can verify the token expiration
#     if time.time() > claims['exp']:
#         return Response('Token is expired',status=403)
#         return False
#     # and the Audience  (use claims['client_id'] if verifying an access token)
#     if claims['aud'] != app_client_id:
#         return Response('Token was not issued for this audience',status=403)
#         return False
#     # now we can use the claims
#     print(claims)
#     return claims

# def login_required(f):
#     @wraps(f)
#     def check_token(*args, **kwargs):
#         try:
#             claims = lambda_handler({'token':request.headers.get('Authorization')})
#             if(isinstance(claims,Response)):
#                 return claims
#             return f(*args, **kwargs)
#         except Exception as e:
#             return Response(str(e),status=500)
#     return check_token

# def admin_required(f):
#     @wraps(f)
#     def check_admin(*args, **kwargs):
#         try:
#             claims = lambda_handler({'token':request.headers.get('Authorization')})            
#             if(isinstance(claims,Response)):
#                 return claims
#             res = (db.session.query(Resource, GeneralCategory)
#             .join(GeneralCategory, Resource.resource_category == GeneralCategory.category_id)
#             .where(GeneralCategory.category_name == 'admin')
#             .where(Resource.primary_email == claims.get('email'))).first()
#             if res == None:
#                 return Response('Need to be an admin to access this request',status=403)
#             return f(*args,**kwargs)
#         except Exception as e:
#             return Response(str(traceback.format_exc()), status=500)
#     return check_admin

# def get_keys_url():
#     region = current_app.config.get("AWS_REGION")
#     userpool_id = current_app.config.get("AWS_USER_POOL_ID")
#     return 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region, userpool_id)

# def refresh_token():
#     try:
#         refresh_token = request.headers.get("Authorization")
#         client = get_cognito_client()
#         try:
#             response = client.initiate_auth(
#             AuthFlow='REFRESH_TOKEN_AUTH',
#             AuthParameters={ 
#             "REFRESH_TOKEN" : refresh_token
#             },
#             ClientId=current_app.config.get("AWS_APP_CLIENT_ID"))
#         except:
#             return Response('Invalid Refresh Token',status=403)
#         id_token = response.get("AuthenticationResult").get("IdToken")
#         return lambda_handler({'token':id_token})
            
#     except Exception as e:
#         return Response(str(traceback.format_exc()), status=500)

# def get_cognito_client():
#     return boto3.client('cognito-idp', 
#     aws_access_key_id=current_app.config.get('AWS_ACCESS_KEY_ID'), 
#     aws_secret_access_key=current_app.config.get('AWS_SECRET_ACCESS_KEY'), 
#     region_name=current_app.config.get('AWS_REGION'))

# def refresh_login_required(f):
#     @wraps(f)
#     def check_token(*args, **kwargs):
#         try:
#             claims = refresh_token()
#             if(isinstance(claims,Response)):
#                 return claims
#             return f(*args, **kwargs)
#         except Exception as e:
#             return Response(str(e),status=500)
#     return check_token

# def refresh_admin_required(f):
#     @wraps(f)
#     def check_admin(*args, **kwargs):
#         try:
#             claims = refresh_token()
#             if(isinstance(claims,Response)):
#                 return claims
#             eprint('claims are', claims)
#             res = (db.session.query(Resource, GeneralCategory)
#             .join(GeneralCategory, Resource.resource_category == GeneralCategory.category_id)
#             .where(GeneralCategory.category_name == 'admin')
#             .where(db.func.trim(Resource.primary_email) == claims.get('email').strip())).first()
#             if res == None:
#                 return Response('Need to be an admin to access this request',status=403)
#             return f(*args,**kwargs)
#         except Exception as e:
#             return Response(str(e),status=500)
#     return check_admin

# def auth_token():
#     try:
#         auth_token = request.headers.get('Authorization')
#         client = get_cognito_client()
#         return client.get_user(AccessToken=auth_token)
#     except Exception as e:
#         return Response('Invalid Access Token',status=403)

# def auth_login_required(f):
#     @wraps(f)
#     def check_token(*args, **kwargs):
#         try:
#             claims = auth_token()
#             if(isinstance(claims,Response)):
#                 return claims
#             return f(*args, **kwargs)
#         except Exception as e:
#             return Response(str(e),status=500)
#     return check_token

# def auth_admin_required(f):
#     @wraps(f)
#     def check_admin(*args, **kwargs):
#         try:
#             claims = auth_token()
#             if(isinstance(claims,Response)):
#                 return claims
#             eprint('claims are', claims)
#             res = (db.session.query(Resource, GeneralCategory)
#             .join(GeneralCategory, Resource.resource_category == GeneralCategory.category_id)
#             .where(GeneralCategory.category_name == 'admin')
#             .where(db.func.trim(Resource.primary_email) == claims.get('Username').strip())).first()
#             if res == None:
#                 return Response('Need to be an admin to access this request',status=403)
#             return f(*args,**kwargs)
#         except Exception as e:
#             return Response(str(e),status=500)
#     return check_admin

        


# # # the following is useful to make this script executable in both
# # # AWS Lambda and any other local environments
# # if __name__ == '__main__':
# #     # for testing locally you can enter the JWT ID Token here
# #     event = {'token': ''}
# #     lambda_handler(event, None)

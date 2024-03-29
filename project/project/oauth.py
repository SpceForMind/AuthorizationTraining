from project import app
from flask import current_app, url_for, request, redirect, session
from rauth import OAuth2Service
import json


class OAuthSignIn(object):
    providers = {}

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        '''Call view <oauth_callback>

        :return url for oauth_callback:
        '''
        return url_for("oauth_callback", provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(self, provider_name):
        '''

        :param provider_name:
        :return realy provider subclass is instance of @provider_name:
        '''
        if provider_name not in self.providers:
            for provider_class in self.__subclasses__():
                provider = provider_class()
                if provider.__repr__() == provider_name:
                    self.providers[provider_name] = provider

        return self.providers[provider_name]


class FacebookSignIn(OAuthSignIn):
    def __init__(self):
        super(FacebookSignIn, self).__init__('facebook')
        self.service = OAuth2Service(
            name='facebook',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://graph.facebook.com/oauth/authorize',
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com/'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        '''OAuth2.0 facebook callback

        :return: tuple (@social_id, @user_login)
        '''
        def decode_json(payload):
            return json.loads(payload.decode("utf-8"))

        if "code" not in request.args:
            return None, None, None

        oauth_session = self.service.get_auth_session(
            data = {"code": request.args["code"],
                    "grant_type": "authorization_code",
                    "redirect_uri": self.get_callback_url()},
            decoder=decode_json
        )
        me = oauth_session.get('me?fields=id,email').json()

        return (
            "facebook$" + me["id"],
            me.get("email").split("@")[0],  # Facebook does not provide
                                            # username, so the email's user
                                            # is used instead
        )

    def __repr__(self):
        return "facebook"


class GithubSignIn(OAuthSignIn):
    def __init__(self):
        super(GithubSignIn, self).__init__("github")
        self.service = OAuth2Service(
            name="github",
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://github.com/login/oauth/authorize',
            access_token_url='https://github.com/login/oauth/access_token',
            base_url='https://api.github.com/'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope="user:email",
            response_type="code",
            redirect_uri=self.get_callback_url()
        ))

    def callback(self):
        '''OAuth2.0 github callback

        :return: tuple (@social_id, @user_login)
        '''
        if "code" not in request.args:
            return None, None, None

        oauth_session = self.service.get_auth_session(
            data={"code": request.args["code"],
                  "grant_type": "authorization_code",
                  "redirect_uri": self.get_callback_url()}
        )

        user = oauth_session.get('user').json()

        return (
            "github$" + str(user["id"]),
            user["login"],
        )

    def __repr__(self):
        return "github"


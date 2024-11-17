import json
import datetime
from cozepy import JWTOAuthApp, Coze, MessageType, TokenAuth, Message, ChatStatus
import config
from cozepy.config import COZE_CN_BASE_URL

class CozeWithOAuthJWT:
    def __init__(self, client_id, private_key, public_key_id):
        self.client_id = client_id
        self.private_key = private_key
        self.public_key_id = public_key_id
        self.oauth_app = self._create_jwt_oauth_app()
        self.access_token = None
        self.coze_client = self._create_coze_client()
        
    def _create_jwt_oauth_app(self):
        """创建并返回一个JWT OAuth App实例"""
        return JWTOAuthApp(
            client_id=self.client_id,
            private_key=self.private_key,
            public_key_id=self.public_key_id,
            base_url=COZE_CN_BASE_URL
        )

    def _get_access_token(self, ttl=3600):
        """使用JWT OAuth App获取access token"""
        return self.oauth_app.get_access_token(ttl)

    def _create_coze_client(self, ttl=3600):
        self.access_token = self._get_access_token(ttl)
        self.coze_client = Coze(auth=TokenAuth(self.access_token.access_token), base_url=COZE_CN_BASE_URL)
        return self.coze_client
 
    def set_app_context(self):
        """设置应用程序上下文，以确保Coze客户端正确运行"""
        # 这里假设您有一个Flask应用程序实例名为app
        # 请根据您的应用程序框架进行相应的上下文设置
        # 例如，在Flask中，您可能会这样做：
        # with self.app.app_context():
        #     # 在这里执行需要应用程序上下文的操作
        #     pass
        pass

    def _ensure_coze_client_not_expired(self):
        if not self.coze_client :
            self.coze_client = self._create_coze_client()
        elif self.access_token.expires_in < datetime.datetime.now().timestamp() :
            self.coze_client = self._create_coze_client()

    def say_hi(self) :
        self._ensure_coze_client_not_expired()

        holiday_question = datetime.datetime.now().strftime('%Y年%m月%d日') + ' '

        chat_poll = self.coze_client.chat.create_and_poll(
            bot_id = config.coze_bot_id,
            user_id = config.coze_user_id,
            additional_messages=[
                Message.build_user_question_text(holiday_question),
            ],
        )

        answer = '{}'
        for message in chat_poll.messages:
            if message.type == MessageType.ANSWER :
                print(message.content)
                answer = message.content
        
        return answer

            #print(message.content, end="", flush=True)
            #print(message.content.tojson().output.result[0].imageUrl)



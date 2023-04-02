from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class TokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        return token


def create_token(user, data_dict={}):
    token = TokenSerializer.get_token(user)
    data_dict["access"] = str(token.access_token)
    data_dict["refresh"] = str(token)
    return data_dict


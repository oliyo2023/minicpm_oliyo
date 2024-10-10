from pocketbase import PocketBase
import const
client = PocketBase(const.PB_URL)
user_data = client.admins.auth_with_password(
    const.Contant.PB_ADMIN_EMAIL, const.Contant.PB_ADMIN_PASSWORD)
def getApiKeyByPlatform(platform):
    try:
        result = client.collection("keys").get_list(1,1,{"filter":'platform="'+platform+'"'})
        if result.total_items > 0:
            return result.items[0].api_key
        else:
            return None
    except Exception as e:
        print(e)
        return None
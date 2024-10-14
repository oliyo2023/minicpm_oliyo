from pocketbase import PocketBase
import const
pb = PocketBase(const.PB_URL)
user_data = pb.admins.auth_with_password(
    const.Contant.PB_ADMIN_EMAIL, const.Contant.PB_ADMIN_PASSWORD)
# 根据平台获取API密钥
def getApiKeyByPlatform(platform):
    try:
        # 从数据库中获取API密钥列表，限制返回数量为1，过滤条件为平台为指定平台
        result = pb.collection("keys").get_list(1,1,{"filter":'platform="'+platform+'"'})
        if result.total_items > 0:
            return result.items[0].api_key
        else:
            return None
    except Exception as e:
        print(e)
        return None
from fastapi import FastAPI, WebSocket
from datetime import datetime
from zhipuai import ZhipuAI
import time
import asyncio
client = ZhipuAI(api_key="d63e4ba96c656df6ba863c0faedcbcf1.0711l2T6EMBsDz7E")
# client = ZhipuAI(api_key="")  # 请填写您自己的API Key
response = client.chat.asyncCompletions.create(
  model="glm-4-0520",  # 填写需要调用的模型编码
  messages=[
        {"role": "user", "content": "请你作为童话故事大王，请以文言文写一篇童话故事，故事的主题是要永远保持一颗善良的心，要能够激发儿童的学习兴趣和想象力，同时也能够帮助儿童更好地理解和接受故事中所蕴含的道理和价值观。"},

  ],
#   stream=False,
)
print(response)
task_id = response.id
task_status = ''
get_cnt = 0

while task_status != 'SUCCESS' and task_status != 'FAILED' and get_cnt <= 40:
    result_response = client.chat.asyncCompletions.retrieve_completion_result(id=task_id)
    print(result_response)
    task_status = result_response.task_status

    time.sleep(2)
    get_cnt += 1
# for chunk in response:
#     print(chunk.choices[0].delta)
# Define a websocket endpoint at `/ws`


# Run the app with `uvicorn main:app --reload`
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# Run the app with `uvicorn main:app --reload`